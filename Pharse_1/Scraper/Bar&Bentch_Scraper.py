#!/usr/bin/env python3
"""Bar &amp; Bench scraper using Playwright for reliable JS-heavy scraping."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from playwright.async_api import Browser, BrowserContext, Page, async_playwright  # type: ignore

from config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

# Bar &amp; Bench category URLs (adapt from inspection)
CATEGORY_URLS = {
    "news": "https://www.barandbench.com/news",
    "columns": "https://www.barandbench.com/columns",
    "judgments": "https://www.barandbench.com/judgments",
}

DEFAULT_MAX_PAGES = DEFAULT_CONFIG.scraper.max_pages
DEFAULT_OUT_FILE = DEFAULT_CONFIG.paths.raw_articles.replace("articles.json", "barbench_articles.json")


def _require_playwright() -> Tuple[type[Browser], type[BrowserContext], type[Page], type[async_playwright]]:
    """Import Playwright async components."""
    try:
        from playwright.async_api import async_playwright, Browser, BrowserContext, Page
        return Browser, BrowserContext, Page, async_playwright
    except ImportError as exc:
        raise ImportError(
            "Playwright is required. Install with `pip install playwright` &amp;&amp; `playwright install`."
        ) from exc


async def scrape_article(page: Page, url: str, *, retries: int = DEFAULT_CONFIG.scraper.retries, base_delay_s: float = DEFAULT_CONFIG.scraper.base_delay_s) -> Optional[Dict[str, Any]]:
    """Extract single article from URL with retries."""
    for attempt in range(retries):
        try:
            await page.goto(url, timeout=DEFAULT_CONFIG.scraper.navigation_timeout_ms, wait_until="domcontentloaded")
            await page.wait_for_timeout(DEFAULT_CONFIG.scraper.page_settle_ms)

            # Bar&amp;Bench selectors (inspect &amp; adapt)
            title = await page.locator("h1.article-title").text_content() or ""
            content = await page.locator(".article-body, .story-body").text_content() or ""
            date_str = await page.locator("time, .date").text_content() or ""

            if not title.strip():
                logger.warning("No title found at %s", url)
                return None

            from utils.date_parser import parse_date
            date = parse_date(date_str) or ""

            article = {
                "url": url,
                "title": title.strip(),
                "content": content.strip(),
                "date": date,
                "source": "barandbench",
                "scraped_at": asyncio.get_event_loop().time(),
            }
            logger.info("Scraped %s", title[:100])
            return article

        except Exception as exc:
            logger.warning("Attempt %d failed for %s: %s", attempt + 1, url, exc)
            await asyncio.sleep(base_delay_s * (2 ** attempt))
    return None


async def _scrape_category_pages(
    context: BrowserContext,
    category_url: str,
    max_pages: int,
    *,
    retries: int = DEFAULT_CONFIG.scraper.retries,
    base_delay_s: float = DEFAULT_CONFIG.scraper.base_delay_s,
) -> List[str]:
    """Extract article URLs from category pagination."""
    page = await context.new_page()
    article_urls = set()

    for page_num in range(1, max_pages + 1):
        url = f"{category_url}/page/{page_num}" if page_num > 1 else category_url
        await page.goto(url, timeout=DEFAULT_CONFIG.scraper.navigation_timeout_ms)

        # Extract links (adapt selectors)
        links = await page.locator("a[href*='/news/'], a[href*='/columns/'], a[href*='/judgments/']").all()
        new_urls = [await link.get_attribute("href") for link in links if link and "http" in (await link.get_attribute("href") or "")]
        article_urls.update(new_urls)
        await asyncio.sleep(DEFAULT_CONFIG.scraper.polite_delay_s)

    await page.close()
    logger.info("Found %d unique article URLs in category", len(article_urls))
    return list(article_urls)


async def scrape(
    *,
    categories: Optional[List[str]] = None,
    out_file: str = DEFAULT_OUT_FILE,
    max_pages: int = DEFAULT_MAX_PAGES,
    concurrency: int = DEFAULT_CONFIG.scraper.concurrency,
    retries: int = DEFAULT_CONFIG.scraper.retries,
    base_delay_s: float = DEFAULT_CONFIG.scraper.base_delay_s,
) -> List[Dict[str, Any]]:
    """Main scraping entrypoint."""
    Browser, BrowserContext, Page, async_playwright = _require_playwright()
    categories = list(categories or CATEGORY_URLS.keys())

    out_file_path = Path(out_file)
    out_file_path.parent.mkdir(parents=True, exist_ok=True)

    all_articles = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context_kwargs = {"user_agent": DEFAULT_CONFIG.scraper.user_agent}
        context = await browser.new_context(**context_kwargs)
        context.set_default_navigation_timeout(DEFAULT_CONFIG.scraper.navigation_timeout_ms)
        context.set_default_timeout(DEFAULT_CONFIG.scraper.navigation_timeout_ms)

        # Gather all article URLs first
        category_urls = [CATEGORY_URLS[cat] for cat in categories]
        all_article_urls = []
        for cat_url in category_urls:
            urls = await _scrape_category_pages(context, cat_url, max_pages, retries=retries, base_delay_s=base_delay_s)
            all_article_urls.extend(urls)

        logger.info("Scraping %d articles with concurrency %d", len(all_article_urls), concurrency)

        semaphore = asyncio.Semaphore(concurrency)
        async def scrape_one(url: str) -> Optional[Dict[str, Any]]:
            async with semaphore:
                page = await context.new_page()
                try:
                    article = await scrape_article(page, url, retries=retries, base_delay_s=base_delay_s)
                    await asyncio.sleep(DEFAULT_CONFIG.scraper.polite_delay_s)
                    return article
                finally:
                    await page.close()

        tasks = [scrape_one(url) for url in all_article_urls[:max_pages * 10]]  # Limit total
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_articles = [r for r in results if not isinstance(r, Exception) and r is not None]

    # Save
    out_file_path.write_text(json.dumps(all_articles, indent=2, ensure_ascii=False))
    logger.info("Saved %d Bar&amp;Bench articles to %s", len(all_articles), out_file)
    return all_articles

