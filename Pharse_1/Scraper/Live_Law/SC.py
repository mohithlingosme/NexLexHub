import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
import os
import hashlib
from datetime import datetime
import random

BASE_URL = "https://www.livelaw.in"
CATEGORY_URLS = [
    "https://www.livelaw.in/supreme-court",
    ]

MAX_PAGES = 10
DATA_FILE = "articles.json"

# 🔁 Proxy Pool
PROXIES = [
    None,  # fallback (no proxy)
    # "http://user:pass@proxy1:port",
    # "http://user:pass@proxy2:port",
]


# =========================
# 🔧 HELPERS
# =========================

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
    return hashlib.md5(title.lower().encode()).hexdigest()


# =========================
# 📥 LOAD EXISTING
# =========================

def load_existing():
    if not os.path.exists(DATA_FILE):
        return {}, set()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    url_map = {a["url"]: a for a in data}
    title_hashes = set(hash_title(a["title"]) for a in data if a.get("title"))

    return url_map, title_hashes


# =========================
# 🔁 RETRY WRAPPER
# =========================

async def retry(func, *args, retries=3):
    for attempt in range(retries):
        try:
            return await func(*args)
        except Exception as e:
            if attempt == retries - 1:
                print(f"❌ Failed after retries: {e}")
                return None
            await asyncio.sleep(2)


# =========================
# 🔗 EXTRACT LINKS
# =========================

async def extract_links(page):
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = normalize_url(a["href"])
        if is_valid_article_url(href):
            links.add(href)

    return links


# =========================
# 🧠 SCRAPE ARTICLE
# =========================

async def scrape_article(context, url):
    page = await context.new_page()

    try:
        await page.goto(url, timeout=60000)
        await asyncio.sleep(1)

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
            data["content"] = clean_text(" ".join(p.get_text() for p in paragraphs))

        # RAG FORMAT 🔥
        data["content"] = f"""
[ARTICLE]
Title: {data['title']}
Date: {data['date']}

[CONTENT]
{data['content']}
"""

        return data

    except Exception as e:
        print(f"❌ Article error: {url} | {e}")
        return None

    finally:
        await page.close()


# =========================
# 💾 SAVE
# =========================

def parse_date(d):
    try:
        return datetime.fromisoformat(d.replace("Z", "+00:00"))
    except:
        return datetime.min


def save_data(data_dict):
    data = list(data_dict.values())
    data.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"💾 Saved {len(data)} articles")


# =========================
# 🚀 MAIN SCRAPER
# =========================

async def scrape():
    existing, title_hashes = load_existing()
    print(f"🔁 Loaded {len(existing)} articles")

    async with async_playwright() as p:
        proxy = random.choice(PROXIES)

        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(proxy={"server": proxy} if proxy else None)
        page = await context.new_page()

        for category in CATEGORY_URLS:
            print(f"\n📂 {category}")

            for i in range(1, MAX_PAGES + 1):
                url = f"{category}?page={i}"

                await retry(page.goto, url)

                links = await extract_links(page)
                print(f"🔗 {len(links)} links")

                tasks = []

                for link in links:
                    if link in existing:
                        continue

                    tasks.append(scrape_article(context, link))

                results = await asyncio.gather(*tasks)

                for article in results:
                    if not article:
                        continue

                    title_hash = hash_title(article["title"])

                    # ❌ skip duplicates
                    if title_hash in title_hashes:
                        continue

                    title_hashes.add(title_hash)
                    existing[article["url"]] = article

                    print(f"✅ {article['title']}")

                save_data(existing)

        await browser.close()


# =========================
# ▶️ RUN
# =========================

if __name__ == "__main__":
    asyncio.run(scrape())