from __future__ import annotations

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
import os
import hashlib
from datetime import datetime
from difflib import SequenceMatcher

# =========================================================
# CONFIG
# =========================================================
BASE_URL = "https://www.barandbench.com"
CATEGORY_URLS = [
    "https://www.barandbench.com/topic/allahabad-high-court",
]

MAX_PAGES = 25
DATA_FILE = r"C:\Users\mohit\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Raw_Data\HighCourt News\AllahabadHC.json"

SIMILARITY_THRESHOLD = 0.90
CONCURRENCY = 3

# =========================================================
# STRICT FILTERING
# =========================================================
INVALID_TITLE_PATTERNS = [
    "Judges",
    "Litigation News",
    "Law & Policy News",
    "Corporate & In-House News",
    "Law Schools News",
    "Columns",
    "Interviews",
    "Advertise",
    "Privacy Policy",
    "Terms of Use",
    "Contact Us",
    "Legal Jobs",
    "Careers",
    "Law School",
    "Student special",
    "Latest Legal News",
    "Working Title",
    "The Recruiters",
    "Dealstreet",
    "News",
    "The Viewpoint",
    "Corporate & In-house Columns",
    "Litigation Columns",
    "Law & Policy Columns",
]

# =========================================================
# HELPERS
# =========================================================
def clean_text(text):
    return " ".join((text or "").split()).strip()


def normalize_url(href):
    if not href:
        return ""
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return urljoin(BASE_URL, href)
    return href.strip()


def is_valid_article_url(url):
    if not url:
        return False

    parsed = urlparse(url)

    if "barandbench.com" not in parsed.netloc:
        return False

    path = parsed.path.lower()

    blocked = [
        "/topic/",
        "/author/",
        "/videos/",
        "/podcasts/",
        "/photos/",
        "/search",
        "/lawschools",
        "/interviews",
        "/columns",
        "/careers",
        "/contact",
        "/advertise",
        "/privacy",
        "/terms",
    ]

    if any(b in path for b in blocked):
        return False

    return path.startswith("/news/")


def is_valid_article(title, url):
    if not title or not url:
        return False

    if not is_valid_article_url(url):
        return False

    title = title.strip().lower()

    for bad in INVALID_TITLE_PATTERNS:
        if bad.lower() == title:
            return False

        if bad.lower() in title and len(title) < 60:
            return False

    return True


def hash_title(title):
    return hashlib.md5(title.lower().encode()).hexdigest()


def hash_content(content):
    return hashlib.md5(content.lower().encode()).hexdigest()


def normalize_title(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def is_similar(a, b):
    return SequenceMatcher(None, a, b).ratio() >= SIMILARITY_THRESHOLD


# =========================================================
# DATE FIX
# =========================================================
def parse_date(d):
    try:
        dt = datetime.fromisoformat(
            d.replace("Z", "+00:00")
        )
        return dt.replace(tzinfo=None)
    except:
        return datetime.min


# =========================================================
# LOAD EXISTING
# =========================================================
def load_existing():
    if not os.path.exists(DATA_FILE):
        return {}, set(), set(), []

    # Handle empty or invalid JSON files
    try:
        if os.path.getsize(DATA_FILE) == 0:
            return {}, set(), set(), []
    except OSError:
        return {}, set(), set(), []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}, set(), set(), []
            parsed = json.loads(content)
            data = parsed if isinstance(parsed, list) else []
    except (json.JSONDecodeError, ValueError):
        # If file is corrupted or has invalid JSON, return empty defaults
        return {}, set(), set(), []

    url_map = {a["url"]: a for a in data if a.get("url")}

    title_hashes = set(
        hash_title(a["title"])
        for a in data
        if a.get("title")
    )

    content_hashes = set(
        hash_content(a["full_text"])
        for a in data
        if a.get("full_text")
    )

    normalized_titles = [
        normalize_title(a["title"])
        for a in data
        if a.get("title")
    ]

    return url_map, title_hashes, content_hashes, normalized_titles


# =========================================================
# SAVE
# =========================================================
def save_data(data_dict):
    data = list(data_dict.values())

    data.sort(
        key=lambda x: parse_date(
            x.get("date", "")
        ),
        reverse=True,
    )

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(f"💾 Saved {len(data)} articles")


# =========================================================
# RESOURCE BLOCKER
# =========================================================
async def block_resources(route):
    if route.request.resource_type in [
        "image",
        "stylesheet",
        "font",
        "media",
    ]:
        await route.abort()
    else:
        await route.continue_()


# =========================================================
# TOPIC PAGE EXTRACTION
# =========================================================
async def extract_links(page):
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    links = set()

    selectors = [
        "h2 a[href]",
        "h3 a[href]",
        "article a[href]",
        "a[href]",
    ]

    for selector in selectors:
        for a in soup.select(selector):
            href = normalize_url(
                a.get("href")
            )

            title = clean_text(
                a.get_text()
            )

            if (
                href
                and is_valid_article(
                    title,
                    href,
                )
            ):
                links.add(href)

    return links


# =========================================================
# ARTICLE SCRAPER
# =========================================================
async def scrape_article(context, url):
    page = await context.new_page()
    await page.route(
        "**/*",
        block_resources,
    )

    try:
        success = False

        for attempt in range(4):
            try:
                await page.goto(
                    url,
                    timeout=90000,
                    wait_until="domcontentloaded",
                )

                success = True
                break

            except:
                await asyncio.sleep(
                    2 + attempt
                )

        if not success:
            print(
                f"❌ Article timeout: {url}"
            )
            return None

        await page.wait_for_timeout(
            5000
        )

        soup = BeautifulSoup(
            await page.content(),
            "html.parser",
        )

        data = {
            "id": hashlib.md5(
                url.encode()
            ).hexdigest(),
            "source": "BarAndBench",
            "url": url,
            "title": "",
            "content": "",
            "full_text": "",
            "summary": "",
            "date": "",
            "author": "",
            "category": "Supreme Court",
            "tags": [],
            "is_live": False,
            "scraped_at": datetime.utcnow().isoformat(),
        }

        # =====================================================
        # JSON-LD EXTRACTION
        # =====================================================
        for script in soup.find_all(
            "script",
            type="application/ld+json",
        ):
            try:
                raw = (
                    script.string
                    or script.get_text(
                        strip=True
                    )
                    or "{}"
                )

                j = json.loads(raw)
                candidates = []

                if isinstance(j, list):
                    candidates.extend(j)

                elif isinstance(j, dict):
                    if (
                        "@graph" in j
                        and isinstance(
                            j["@graph"],
                            list,
                        )
                    ):
                        candidates.extend(
                            j["@graph"]
                        )
                    else:
                        candidates.append(
                            j
                        )

                for item in candidates:
                    if not isinstance(
                        item,
                        dict,
                    ):
                        continue

                    if item.get(
                        "@type"
                    ) not in [
                        "NewsArticle",
                        "Article",
                        "LiveBlogPosting",
                    ]:
                        continue

                    data["title"] = clean_text(
                        item.get(
                            "headline",
                            "",
                        )
                        or item.get(
                            "name",
                            "",
                        )
                    )

                    data["content"] = clean_text(
                        item.get(
                            "articleBody",
                            "",
                        )
                        or item.get(
                            "description",
                            "",
                        )
                        or item.get(
                            "abstract",
                            "",
                        )
                        or item.get(
                            "text",
                            "",
                        )
                    )

                    data["date"] = (
                        item.get(
                            "datePublished",
                            "",
                        )
                        or item.get(
                            "dateModified",
                            "",
                        )
                        or item.get(
                            "coverageStartTime",
                            "",
                        )
                    )

                    if isinstance(
                        item.get("author"),
                        dict,
                    ):
                        data["author"] = clean_text(
                            item[
                                "author"
                            ].get(
                                "name", ""
                            )
                        )

                    if (
                        item.get("@type")
                        == "LiveBlogPosting"
                    ):
                        data[
                            "is_live"
                        ] = True

                    break

            except:
                continue

        # =====================================================
        # FALLBACK TITLE
        # =====================================================
        if not data["title"]:
            h1 = soup.find("h1")
            if h1:
                data["title"] = clean_text(
                    h1.get_text()
                )

        # =====================================================
        # FALLBACK DATE
        # =====================================================
        if not data["date"]:
            meta = (
                soup.find(
                    "meta",
                    property="article:published_time",
                )
                or soup.find(
                    "meta",
                    attrs={
                        "name": "publish-date"
                    },
                )
            )

            if meta:
                data["date"] = meta.get(
                    "content", ""
                )

        # =====================================================
        # DOM FALLBACK
        # =====================================================
        if len(data["content"]) < 100:
            candidate_paragraphs = []

            selectors = [
                "div.story-element.story-element-text",
                "div.story-element-text",
                "div.story-element",
                "div[itemprop='articleBody']",
                "article",
                "div[data-content]",
                "div[class*='story']",
                "div[class*='content']",
                "section",
            ]

            for selector in selectors:
                blocks = soup.select(
                    selector
                )

                for block in blocks:
                    paragraphs = (
                        block.find_all(
                            "p"
                        )
                    )

                    for p in paragraphs:
                        txt = clean_text(
                            p.get_text()
                        )

                        if len(txt) > 15:
                            candidate_paragraphs.append(
                                txt
                            )

                if candidate_paragraphs:
                    break

            if not candidate_paragraphs:
                for p in soup.find_all("p"):
                    txt = clean_text(
                        p.get_text()
                    )

                    if len(txt) > 15:
                        candidate_paragraphs.append(
                            txt
                        )

            data["content"] = clean_text(
                " ".join(
                    candidate_paragraphs
                )
            )

        # =====================================================
        # FINAL VALIDATION
        # =====================================================
        if not is_valid_article(
            data["title"],
            url,
        ):
            return None

        if (
            not data["title"]
            or not data["content"]
        ):
            return None

        # KEEP OUTPUT SAME
        data["summary"] = data["content"][:1000]
        data["full_text"] = data["content"]

        data["content"] = f"""
[ARTICLE]
Title: {data['title']}
Date: {data['date']}
Source: BarAndBench

[CONTENT]
{data['full_text']}
"""

        return data

    except Exception as e:
        print(
            f"❌ Article error: {url} | {e}"
        )
        return None

    finally:
        await page.close()


# =========================================================
# MAIN SCRAPER
# =========================================================
async def scrape():
    (
        existing,
        title_hashes,
        content_hashes,
        normalized_titles,
    ) = load_existing()

    print(
        f"🔁 Loaded {len(existing)} articles"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )

        context = (
            await browser.new_context()
        )

        page = await context.new_page()
        await page.route(
            "**/*",
            block_resources,
        )

        for category in CATEGORY_URLS:
            print(f"\n📂 {category}")

            previous_fingerprint = None

            for i in range(
                1,
                MAX_PAGES + 1,
            ):
                url = (
                    category
                    if i == 1
                    else f"{category}?page={i}"
                )

                try:
                    await page.goto(
                        url,
                        timeout=90000,
                        wait_until="domcontentloaded",
                    )
                except:
                    continue

                await page.wait_for_timeout(
                    3000
                )

                links = await extract_links(
                    page
                )

                topic_fingerprint = hash(
                    tuple(
                        sorted(links)
                    )
                )

                if (
                    not links
                    or topic_fingerprint
                    == previous_fingerprint
                ):
                    print(
                        "⛔ Stopping due to stale or duplicate topic pages"
                    )
                    break

                previous_fingerprint = (
                    topic_fingerprint
                )

                print(
                    f"🔗 Page {i}: {len(links)} links"
                )

                semaphore = asyncio.Semaphore(
                    CONCURRENCY
                )

                async def bounded_scrape(
                    link,
                ):
                    async with semaphore:
                        return await scrape_article(
                            context,
                            link,
                        )

                tasks = []

                for link in links:
                    if link in existing:
                        continue

                    tasks.append(
                        bounded_scrape(
                            link
                        )
                    )

                results = await asyncio.gather(
                    *tasks
                )

                for article in results:
                    if not article:
                        continue

                    title_hash = hash_title(
                        article["title"]
                    )

                    content_hash = (
                        hash_content(
                            article[
                                "full_text"
                            ]
                        )
                    )

                    normalized = (
                        normalize_title(
                            article[
                                "title"
                            ]
                        )
                    )

                    if (
                        title_hash
                        in title_hashes
                    ):
                        continue

                    if (
                        content_hash
                        in content_hashes
                    ):
                        continue

                    if any(
                        is_similar(
                            normalized,
                            prev,
                        )
                        for prev in normalized_titles[
                            -150:
                        ]
                    ):
                        continue

                    title_hashes.add(
                        title_hash
                    )

                    content_hashes.add(
                        content_hash
                    )

                    normalized_titles.append(
                        normalized
                    )

                    existing[
                        article["url"]
                    ] = article

                    print(
                        f"✅ {article['title']}"
                    )

                save_data(existing)

        await browser.close()


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    asyncio.run(scrape())