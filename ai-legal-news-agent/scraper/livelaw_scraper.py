import asyncio
import logging
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
import os
import hashlib
from datetime import datetime
import random
from utils.file_utils import save_json, load_json
from utils.date_parser import parse_date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.livelaw.in"
CATEGORY_URLS = [
    "https://www.livelaw.in/news-updates",
    "https://www.livelaw.in/top-stories",
    "https://www.livelaw.in/supreme-court",
    "https://www.livelaw.in/high-court/karnataka-high-court",
    "https://www.livelaw.in/high-court",
    "https://www.livelaw.in/articles",
    "https://www.livelaw.in/digests",
    "https://www.livelaw.in/consumer-cases",
    "https://www.livelaw.in/book-reviews",
    "https://www.livelaw.in/round-ups",
    "https://www.livelaw.in/more/international",
    "https://www.livelaw.in/ibc-cases",
    "https://www.livelaw.in/arbitration-cases",
    "https://www.livelaw.in/labour-service",
    "https://www.livelaw.in/tech-law",
    "https://www.livelaw.in/corporate-law"
]

MAX_PAGES = 10
DATA_FILE = "data/raw/articles.json"

PROXIES = [None]  # Add proxies if needed

def clean_text(text):
    return " ".join(text.split()).strip()

def normalize_url(href):
    if not href:
        return ""
    if href.startswith("/"):
        return urljoin(BASE_URL, href)
    return href

def is_valid_article_url(url):
    if not url:
        return False
    parsed = urlparse(url)
    return "livelaw.in" in parsed.netloc and re.search(r"-\d+$", parsed.path)

def hash_title(title):
    text = title.lower()
    return hashlib.md5(text.encode()).hexdigest()

async def retry(func, *args, retries=3):
    for attempt in range(retries):
        try:
            return await func(*args)
        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {e}")
            if attempt == retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)

async def extract_links(page):
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = normalize_url(a["href"])
        if is_valid_article_url(href):
            links.add(href)
    return links

async def scrape_article(context, url):
    page = await context.new_page()
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(1000)
        soup = BeautifulSoup(await page.content(), "html.parser")
        data = {
            "url": url,
            "title": "",
            "content": "",
            "date": "",
            "description": "",
            "image": "",
            "category": "",
            "tags": []
        }
        # JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                j = json.loads(script.string)
                if isinstance(j, list):
                    j = j[0]
                if j.get("@type") in ["NewsArticle", "Article"]:
                    data["title"] = j.get("headline", "")
                    data["content"] = clean_text(j.get("articleBody", ""))
                    data["date"] = j.get("datePublished", "")
                    data["description"] = j.get("description", "")
                    break
            except:
                continue
        # Fallbacks
        if not data["title"]:
            h1 = soup.find("h1")
            if h1:
                data["title"] = clean_text(h1.get_text())
        if not data["content"]:
            paragraphs = soup.find_all("p")
            data["content"] = clean_text(" ".join(p.get_text() for p in paragraphs[:20]))
        # RAG format
        data["scraped_at"] = datetime.now().isoformat()
        logger.info(f"Scraped: {data['title'][:50]}...")
        return data
    except Exception as e:
        logger.error(f"Article error {url}: {e}")
        return None
    finally:
        await page.close()

async def scrape():
    try:
        existing_data = load_json(DATA_FILE)
        existing = {a["url"]: a for a in existing_data if "url" in a}
        title_hashes = {hash_title(a["title"]): True for a in existing_data if "title" in a}
        logger.info(f"Loaded {len(existing)} articles")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            all_articles = list(existing.values())
            
            for category in CATEGORY_URLS:
                logger.info(f"Scraping {category}")
                for i in range(1, MAX_PAGES + 1):
                    url = f"{category}?page={i}"
                    await retry(page.goto, url)
                    
                    links = await extract_links(page)
                    logger.info(f"Found {len(links)} links")
                    
                    tasks = []
                    for link in links:
                        if link not in existing:
                            tasks.append(scrape_article(context, link))
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for article in results:
                        if isinstance(article, Exception):
                            continue
                        if not article:
                            continue
                        title_hash = hash_title(article["title"])
                        if title_hash in title_hashes:
                            continue
                        title_hashes.add(title_hash)
                        all_articles.append(article)
                        logger.info(f"Added: {article['title'][:50]}")
                    
                    await asyncio.sleep(2)  # Rate limit
            
            all_articles.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
            save_json(all_articles, DATA_FILE)
            logger.info("Scraping complete!")
            
            await browser.close()
    except Exception as e:
        logger.error(f"Scrape failed: {e}")

if __name__ == "__main__":
    asyncio.run(scrape())

