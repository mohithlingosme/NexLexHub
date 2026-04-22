import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from config import DEFAULT_CONFIG
from utils.date_parser import parse_date
from utils.file_utils import load_json, normalize_text, save_json

logger = logging.getLogger(__name__)

BASE_URL = "https://www.livelaw.in"

CATEGORY_URLS = [
    "https://www.livelaw.in/news-updates",
    "https://www.livelaw.in/top-stories",
    "https://www.livelaw.in/supreme-court",
    "https://www.livelaw.in/high-court",
    "https://www.livelaw.in/articles",
    "https://www.livelaw.in/digests",
    "https://www.livelaw.in/consumer-cases",
    "https://www.livelaw.in/round-ups",
    "https://www.livelaw.in/more/international",
    "https://www.livelaw.in/ibc-cases",
    "https://www.livelaw.in/arbitration-cases",
    "https://www.livelaw.in/labour-service",
    "https://www.livelaw.in/tech-law",
    "https://www.livelaw.in/corporate-law",
]

DEFAULT_MAX_PAGES = DEFAULT_CONFIG.scraper.max_pages
DEFAULT_OUT_FILE = DEFAULT_CONFIG.paths.raw_articles

_ARTICLE_ID_RE = re.compile(r"-\d+$")


def _require_playwright() -> Tuple[Any, Any, Any, Any]:
    """
    Import Playwright lazily so non-scrape steps (clean/dedup/chunk/summarize)
    can run without the heavy Playwright dependency.
    """
    try:
        from playwright.async_api import Browser, BrowserContext, Page, async_playwright  # type: ignore

        return Browser, BrowserContext, Page, async_playwright
    except Exception as exc:
        raise RuntimeError(
            "Playwright is required for scraping. Install deps with `pip install -r requirements.txt` "
            "and install browsers with `playwright install`."
        ) from exc


def _normalize_url(href: str) -> str:
    href = (href or "").strip()
    if not href:
        return ""
    if href.startswith("/"):
        return urljoin(BASE_URL, href)
    return href


def _is_valid_article_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    if "livelaw.in" not in parsed.netloc:
        return False
    return bool(_ARTICLE_ID_RE.search(parsed.path))


async def _with_retries(
    coro_factory,
    *,
    retries: int = DEFAULT_CONFIG.scraper.retries,
    base_delay_s: float = DEFAULT_CONFIG.scraper.base_delay_s,
):
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            return await coro_factory()
        except Exception as exc:
            last_exc = exc
            delay = base_delay_s * (2**attempt)
            logger.warning("Retry %d/%d failed: %s", attempt + 1, retries, str(exc))
            await asyncio.sleep(delay)
    raise last_exc  # type: ignore[misc]


async def _extract_listing_links(page: Any) -> Set[str]:
    html = await page.content()
    soup = BeautifulSoup(html, "lxml")

    links: Set[str] = set()
    for a in soup.find_all("a", href=True):
        href = _normalize_url(a.get("href", ""))
        if _is_valid_article_url(href):
            links.add(href)
    return links


def _extract_jsonld_article(soup: BeautifulSoup) -> Dict[str, Any]:
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        candidates: List[Dict[str, Any]] = []
        if isinstance(data, dict):
            candidates = [data]
        elif isinstance(data, list):
            candidates = [d for d in data if isinstance(d, dict)]

        for obj in candidates:
            typ = obj.get("@type")
            if typ in ("NewsArticle", "Article"):
                return obj
    return {}


def _extract_article_body(soup: BeautifulSoup) -> str:
    # Try known-ish containers first, then fall back to all <p>.
    containers = []
    for sel in [
        "article",
        ".details-content",
        ".details-news",
        ".article-content",
        ".article_body",
        ".post-content",
        ".content",
    ]:
        node = soup.select_one(sel)
        if node is not None:
            containers.append(node)

    if not containers:
        containers = [soup]

    paras: List[str] = []
    for container in containers:
        for p in container.find_all("p"):
            txt = normalize_text(p.get_text(" ", strip=True))
            if not txt:
                continue
            # Filter obvious boilerplate lines.
            if txt.lower() in ("advertisement", "subscribe", "follow us"):
                continue
            paras.append(txt)
        if len(" ".join(paras)) >= 800:
            break

    return normalize_text("\n\n".join(paras))


def _extract_title(soup: BeautifulSoup, jsonld: Dict[str, Any]) -> str:
    title = normalize_text(jsonld.get("headline", ""))
    if title:
        return title

    h1 = soup.find("h1")
    if h1:
        title = normalize_text(h1.get_text(" ", strip=True))
    return title


def _extract_date(soup: BeautifulSoup, jsonld: Dict[str, Any]) -> str:
    date = normalize_text(jsonld.get("datePublished", "")) or normalize_text(jsonld.get("dateCreated", ""))
    if date:
        return date

    meta = soup.find("meta", attrs={"property": "article:published_time"})
    if meta and meta.get("content"):
        return normalize_text(meta["content"])

    time_el = soup.find("time")
    if time_el:
        return normalize_text(time_el.get("datetime") or time_el.get_text(" ", strip=True))

    return ""


async def _scrape_article(context: Any, url: str, category: str) -> Optional[Dict[str, Any]]:
    page = await context.new_page()
    try:
        await _with_retries(
            lambda: page.goto(
                url,
                timeout=DEFAULT_CONFIG.scraper.navigation_timeout_ms,
                wait_until="domcontentloaded",
            )
        )
        await page.wait_for_timeout(DEFAULT_CONFIG.scraper.page_settle_ms)  # let late JS settle

        html = await page.content()
        soup = BeautifulSoup(html, "lxml")

        jsonld = _extract_jsonld_article(soup)
        title = _extract_title(soup, jsonld)
        content = normalize_text(jsonld.get("articleBody", "")) or _extract_article_body(soup)
        date = _extract_date(soup, jsonld)

        if not title or not content:
            return None

        return {
            "url": url,
            "title": title,
            "content": content,
            "date": date,
            "category": category,
            "scraped_at": datetime.utcnow().isoformat(),
        }
    except Exception as exc:
        logger.warning("Failed to scrape article %s: %s", url, str(exc))
        return None
    finally:
        await page.close()


async def scrape(
    *,
    categories: Optional[Iterable[str]] = None,
    max_pages: int = DEFAULT_MAX_PAGES,
    out_file: str = DEFAULT_OUT_FILE,
    concurrency: int = DEFAULT_CONFIG.scraper.concurrency,
) -> List[Dict[str, Any]]:
    _, _, _, async_playwright = _require_playwright()
    categories = list(categories) if categories is not None else list(CATEGORY_URLS)

    existing_data = load_json(out_file, default=[])
    existing_by_url = {a.get("url"): a for a in existing_data if isinstance(a, dict) and a.get("url")}

    sem = asyncio.Semaphore(concurrency)

    async def bounded_scrape(ctx: Any, link: str, cat: str):
        async with sem:
            return await _scrape_article(ctx, link, cat)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        context.set_default_navigation_timeout(DEFAULT_CONFIG.scraper.navigation_timeout_ms)
        context.set_default_timeout(DEFAULT_CONFIG.scraper.navigation_timeout_ms)

        # Speed/reliability: block non-essential heavy resources.
        async def _route(route, request):
            try:
                if request.resource_type in ("image", "media", "font"):
                    await route.abort()
                else:
                    await route.continue_()
            except Exception:
                try:
                    await route.continue_()
                except Exception:
                    pass

        await context.route("**/*", _route)
        page = await context.new_page()

        try:
            all_articles: List[Dict[str, Any]] = list(existing_by_url.values())

            for category in categories:
                logger.info("Listing: %s", category)
                for i in range(1, max_pages + 1):
                    listing_url = f"{category}?page={i}"
                    try:
                        await _with_retries(
                            lambda: page.goto(
                                listing_url,
                                timeout=DEFAULT_CONFIG.scraper.navigation_timeout_ms,
                                wait_until="domcontentloaded",
                            )
                        )
                    except Exception as exc:
                        logger.warning("Listing page failed: %s (%s)", listing_url, str(exc))
                        continue

                    links = await _extract_listing_links(page)
                    new_links = [l for l in links if l not in existing_by_url]
                    if not new_links:
                        continue

                    tasks = [bounded_scrape(context, link, category) for link in sorted(new_links)]
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for result in results:
                        if isinstance(result, Exception) or not result:
                            continue
                        existing_by_url[result["url"]] = result
                        all_articles.append(result)

                    # Save incrementally so partial runs still produce output.
                    all_articles.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
                    save_json(all_articles, out_file)

                    await asyncio.sleep(DEFAULT_CONFIG.scraper.polite_delay_s)  # polite pacing

            all_articles.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
            save_json(all_articles, out_file)
            return all_articles
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(scrape())

