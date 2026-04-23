from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import hashlib
import json
import re
import time
import os

# =========================
# 🔧 CONFIG
# =========================

BASE_URL = "https://www.livelaw.in"
CATEGORY_URL = "https://www.livelaw.in/supreme-court"

MAX_PAGES = 20
DAYS_LIMIT = 7

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data", "Raw_Data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "SC_articles.json")


# =========================
# 🧠 HELPERS
# =========================

def clean_text(text):
    return " ".join(text.split()).strip()


def normalize_url(href):
    if not href:
        return ""
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return urljoin(BASE_URL, href)
    return href


def is_valid_article_url(url):
    if not url:
        return False

    parsed = urlparse(url)

    if "livelaw.in" not in parsed.netloc:
        return False

    path = parsed.path.lower()

    if "/supreme-court/" not in path:
        return False

    if any(x in path for x in ["/more/", "/tag/", "/category/", "/login"]):
        return False

    return bool(re.search(r"-\d+$", path))


def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        return None


def is_recent(date_str):
    dt = parse_date(date_str)
    if not dt:
        return False
    return dt >= datetime.now(dt.tzinfo) - timedelta(days=DAYS_LIMIT)


# =========================
# 🔥 DEDUP ENGINE
# =========================

def generate_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def is_similar(t1, t2, threshold=0.85):
    return SequenceMatcher(None, t1, t2).ratio() > threshold


def is_duplicate(article, existing_map, hash_set):
    if article["url"] in existing_map:
        return True

    content_hash = generate_hash(article["content"])
    if content_hash in hash_set:
        return True

    for existing in existing_map.values():
        if is_similar(article["title"], existing["title"]):
            return True

    return False


# =========================
# 📥 SAFE LOAD
# =========================

def load_existing():
    if not os.path.exists(OUTPUT_FILE):
        return {}, set()

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return {}, set()

            data = json.loads(content)

            url_map = {a["url"]: a for a in data}

            hash_set = set()
            for a in data:
                if "content" in a:
                    hash_set.add(generate_hash(a["content"]))

            return url_map, hash_set

    except:
        print("⚠️ Corrupted JSON → resetting")
        return {}, set()


# =========================
# 💾 SAFE SAVE
# =========================

def save_data(data_dict):
    data = list(data_dict.values())

    data.sort(
        key=lambda x: parse_date(x.get("date", "")) or datetime.min,
        reverse=True
    )

    temp_file = OUTPUT_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    os.replace(temp_file, OUTPUT_FILE)

    print(f"💾 Saved {len(data)} articles")


# =========================
# 🔗 EXTRACT LINKS
# =========================

def extract_links(page):
    soup = BeautifulSoup(page.content(), "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = normalize_url(a["href"])

        if is_valid_article_url(href):
            links.add(href)

    return links


# =========================
# 📰 SCRAPE ARTICLE
# =========================

def scrape_article(page, url, retries=3):
    for attempt in range(retries):
        try:
            page.goto(url, timeout=60000)
            time.sleep(1)

            soup = BeautifulSoup(page.content(), "html.parser")

            scripts = soup.find_all("script", type="application/ld+json")

            for script in scripts:
                try:
                    data = json.loads(script.string)

                    if isinstance(data, list):
                        data = data[0]

                    if data.get("@type") == "NewsArticle":
                        return {
                            "url": url,
                            "title": data.get("headline", ""),
                            "content": clean_text(data.get("articleBody", "")),
                            "date": data.get("datePublished", "")
                        }

                except:
                    continue

            return None

        except:
            print(f"⚠️ Retry {attempt+1}: {url}")
            time.sleep(2)

    print(f"❌ Failed: {url}")
    return None


# =========================
# 📂 SCRAPER CORE
# =========================

def scrape(page, existing, hash_set):
    for i in range(1, MAX_PAGES + 1):
        url = f"{CATEGORY_URL}?page={i}"
        print(f"\n📂 {url}")

        try:
            page.goto(url, timeout=60000)
        except:
            print("⚠️ Page load failed")
            continue

        time.sleep(2)

        links = extract_links(page)
        print(f"Found {len(links)} links")

        recent_found = False

        for link in links:
            article = scrape_article(page, link)

            if not article:
                continue

            if not is_recent(article["date"]):
                continue

            recent_found = True

            if is_duplicate(article, existing, hash_set):
                print("⚠️ Duplicate skipped")
                continue

            existing[link] = article
            hash_set.add(generate_hash(article["content"]))

            print(f"✅ {article['title'][:60]}")

            save_data(existing)
            time.sleep(1)

        if not recent_found:
            print("⛔ No recent articles → stopping")
            break


# =========================
# 🚀 MAIN
# =========================

def main():
    existing, hash_set = load_existing()
    print(f"🔁 Loaded {len(existing)} articles")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        scrape(page, existing, hash_set)

        browser.close()

    save_data(existing)


# =========================
# ▶️ RUN
# =========================

if __name__ == "__main__":
    main()
