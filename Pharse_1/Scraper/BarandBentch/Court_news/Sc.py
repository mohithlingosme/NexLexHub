from dataclasses import dataclass
from typing import Optional, Dict
from pathlib import Path
import asyncio
import argparse
import logging
import hashlib
import json
import sqlite3
import re

from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright, Browser
from bs4 import BeautifulSoup


# =========================================================
# CONFIG
# =========================================================

@dataclass
class Config:
    base_url: str = "https://www.barandbench.com"
    category_url: str = "https://www.barandbench.com/topic/supreme-court-of-india"
    max_pages: int = 25
    days_limit: int = 7
    scrape_timeout: int = 60000
    scrape_retries: int = 3
    headless: bool = True
    concurrency: int = 6
    stale_page_limit: int = 3

    data_dir: Path = Path(__file__).parent / "Data" / "Raw_Data"
    db_file: Path = None
    log_file: Path = None

    def __post_init__(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.data_dir / "BB_SC_articles.db"
        self.log_file = self.data_dir.parent / "logs" / "bb_scraper.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)


# =========================================================
# ARTICLE MODEL
# =========================================================

@dataclass
class Article:
    url: str
    title: str
    content: str
    date: str

    def parse_date(self) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(self.date.replace("Z", "+00:00"))
        except Exception:
            return None

    def is_recent(self, days_limit: int) -> bool:
        dt = self.parse_date()
        if not dt:
            return False
        return dt >= datetime.now(timezone.utc) - timedelta(days=days_limit)


# =========================================================
# UTILITIES
# =========================================================

def setup_logging(config: Config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(config.log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_url(href: str, base_url: str) -> str:
    if not href:
        return ""
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return urljoin(base_url, href)
    return href


def is_valid_article_url(url: str) -> bool:
    parsed = urlparse(url)

    if "barandbench.com" not in parsed.netloc:
        return False

    path = parsed.path.lower()

    blocked = [
        "/topic/",
        "/author/",
        "/podcasts/",
        "/columns/",
        "/interviews/",
        "/videos/",
        "/tags/",
        "/search"
    ]

    if any(b in path for b in blocked):
        return False

    # Bar & Bench article URLs generally contain year/month/day slug structure
    return bool(re.search(r"/\d{4}/\d{2}/\d{2}/", path))


def generate_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


# =========================================================
# DATABASE
# =========================================================

class ArticleDatabase:
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                title_hash TEXT,
                content TEXT,
                content_hash TEXT,
                date TEXT,
                scraped_at TEXT
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        self.conn.commit()

    def article_exists(self, url: str) -> bool:
        cur = self.conn.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
        return cur.fetchone() is not None

    def is_duplicate(self, article: Article) -> bool:
        cur = self.conn.execute(
            "SELECT 1 FROM articles WHERE title_hash = ? OR content_hash = ?",
            (normalize_title(article.title), generate_hash(article.content))
        )
        return cur.fetchone() is not None

    def insert_article(self, article: Article):
        self.conn.execute("""
            INSERT OR IGNORE INTO articles
            (url, title, title_hash, content, content_hash, date, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article.url,
            article.title,
            normalize_title(article.title),
            article.content,
            generate_hash(article.content),
            article.date,
            datetime.now(timezone.utc).isoformat()
        ))
        self.conn.commit()

    def update_last_scrape(self):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_scrape_date', ?)",
            (now,)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


# =========================================================
# RESOURCE BLOCKING
# =========================================================

async def block_resources(route):
    if route.request.resource_type in ["image", "font", "stylesheet", "media"]:
        await route.abort()
    else:
        await route.continue_()


# =========================================================
# ARTICLE SCRAPER
# =========================================================

async def scrape_article(browser: Browser, url: str, config: Config) -> Optional[Article]:
    for attempt in range(config.scrape_retries):
        page = await browser.new_page()
        await page.route("**/*", block_resources)

        try:
            await page.goto(url, timeout=config.scrape_timeout)
            await page.wait_for_timeout(1200)

            soup = BeautifulSoup(await page.content(), "html.parser")

            # Bar & Bench heavily uses JSON-LD structured data
            for script in soup.find_all("script", {"type": "application/ld+json"}):
                try:
                    raw = script.string or "{}"
                    data = json.loads(raw)

                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("@type") == "NewsArticle":
                                data = item
                                break

                    if isinstance(data, dict) and data.get("@type") == "NewsArticle":
                        title = clean_text(data.get("headline", ""))
                        content = clean_text(data.get("articleBody", ""))
                        date = data.get("datePublished", "")

                        if title and content:
                            return Article(
                                url=url,
                                title=title,
                                content=content,
                                date=date
                            )
                except Exception:
                    continue

            # Fallback HTML parsing
            title_tag = soup.find("h1")
            body_div = soup.find("div", class_=re.compile(r"story|article|content", re.I))
            date_meta = soup.find("meta", {"property": "article:published_time"})

            if title_tag and body_div:
                paragraphs = body_div.find_all("p")
                content = clean_text(" ".join(p.get_text(" ", strip=True) for p in paragraphs))

                return Article(
                    url=url,
                    title=clean_text(title_tag.get_text()),
                    content=content,
                    date=date_meta.get("content", "") if date_meta else ""
                )

        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed for {url}: {e}")
            await asyncio.sleep(2)

        finally:
            await page.close()

    logging.error(f"All retries failed for {url}")
    return None


# =========================================================
# PAGE PROCESSOR
# =========================================================

async def process_page(browser, db, page_num, config, sem, stats):
    page = await browser.new_page()
    await page.route("**/*", block_resources)

    page_url = f"{config.category_url}?page={page_num}"

    try:
        await page.goto(page_url, timeout=config.scrape_timeout)
        await page.wait_for_timeout(1500)

        soup = BeautifulSoup(await page.content(), "html.parser")

        links = {
            normalize_url(a.get("href"), config.base_url)
            for a in soup.find_all("a", href=True)
            if is_valid_article_url(normalize_url(a.get("href"), config.base_url))
        }

        existing_links = [l for l in links if db.article_exists(l)]
        new_links = [l for l in links if not db.article_exists(l)]

        logging.info(
            f"Page {page_num}: {len(new_links)} new | {len(existing_links)} existing skipped"
        )

        if not new_links:
            return False

        async def bounded_scrape(link):
            async with sem:
                return await scrape_article(browser, link, config)

        tasks = [bounded_scrape(link) for link in new_links]
        articles = await asyncio.gather(*tasks, return_exceptions=True)

        recent_found = 0

        for art in articles:
            if not isinstance(art, Article):
                continue

            if art.is_recent(config.days_limit):
                recent_found += 1
                stats["recent"] += 1

                if not db.is_duplicate(art):
                    db.insert_article(art)
                    stats["new"] += 1
                    logging.info(f"Added: {art.title[:90]}")
                else:
                    stats["dup"] += 1

        return recent_found > 0

    except Exception as e:
        logging.error(f"Page {page_num} failed: {e}")
        return False

    finally:
        await page.close()


# =========================================================
# MAIN LOOP
# =========================================================

async def scrape(config: Config):
    db = ArticleDatabase(config.db_file)

    stats = {
        "new": 0,
        "dup": 0,
        "recent": 0
    }

    stale_pages = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config.headless)
        sem = asyncio.Semaphore(config.concurrency)

        for page_num in range(1, config.max_pages + 1):
            should_continue = await process_page(
                browser,
                db,
                page_num,
                config,
                sem,
                stats
            )

            if not should_continue:
                stale_pages += 1
            else:
                stale_pages = 0

            if stale_pages >= config.stale_page_limit:
                logging.info("Stopping due to stale pages")
                break

            await asyncio.sleep(1)

        await browser.close()

    db.update_last_scrape()
    db.close()

    logging.info(
        f"Scrape complete | New: {stats['new']} | Duplicates: {stats['dup']} | Recent: {stats['recent']}"
    )


# =========================================================
# CLI
# =========================================================

def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="Bar & Bench Supreme Court Incremental Scraper"
    )

    parser.add_argument("--max-pages", type=int, default=25)
    parser.add_argument("--days-limit", type=int, default=7)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--concurrency", type=int, default=6)

    args = parser.parse_args()

    config = Config()
    config.max_pages = args.max_pages
    config.days_limit = args.days_limit
    config.headless = args.headless or config.headless
    config.concurrency = args.concurrency

    if args.data_dir:
        config.data_dir = args.data_dir
        config.__post_init__()

    return config


def main():
    config = parse_args()
    setup_logging(config)

    logging.info("Starting Bar & Bench Supreme Court scraper")

    asyncio.run(scrape(config))


if __name__ == "__main__":
    main()
