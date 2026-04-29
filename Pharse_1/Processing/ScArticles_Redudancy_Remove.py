import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Dict, Set


# =========================================================
# CONFIG
# =========================================================

RAW_FILE = Path("C:\Users\mohit\Documents\GitHub\NexLexHub\Pharse_1\Scraper\Data\Raw_Data\articles.json")
OUTPUT_FILE = Path("Nr_Sc_Articles.json")
SIMILARITY_THRESHOLD = 0.88


# =========================================================
# UTILITIES
# =========================================================

def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_title(title: str) -> str:
    """Normalize title for duplicate comparison"""
    title = title.lower()
    title = re.sub(r"\.\.\.|:.*$", "", title)  # remove trailing truncation / subtitles
    title = re.sub(r"[^a-z0-9]", "", title)
    return title


def generate_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def is_similar(t1: str, t2: str, threshold: float) -> bool:
    return SequenceMatcher(None, t1, t2).ratio() >= threshold


def parse_date(date_str: str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.min


def is_valid_sc_article(article: Dict) -> bool:
    """
    Optional stricter SC filtering.
    Excludes weekly digests / roundups / non-case articles.
    """
    title = article.get("title", "").lower()

    blocked_keywords = [
        "weekly digest",
        "daily round-up",
        "daily roundup",
        "top stories",
        "round-up",
        "weekly roundup"
    ]

    return not any(keyword in title for keyword in blocked_keywords)


# =========================================================
# MAIN DEDUPER
# =========================================================

def dedupe_articles(raw_articles: List[Dict]) -> List[Dict]:
    seen_urls: Set[str] = set()
    seen_content_hashes: Set[str] = set()
    seen_titles: List[str] = []

    cleaned_articles: List[Dict] = []

    stats = {
        "total": 0,
        "url_duplicates": 0,
        "content_duplicates": 0,
        "title_similar_duplicates": 0,
        "filtered_non_sc": 0,
        "retained": 0
    }

    # Sort newest first
    raw_articles.sort(
        key=lambda x: parse_date(x.get("date", "")),
        reverse=True
    )

    for article in raw_articles:
        stats["total"] += 1

        url = article.get("url", "").strip()
        title = clean_text(article.get("title", ""))
        content = clean_text(article.get("content", ""))
        date = article.get("date", "")

        if not url or not title or not content:
            continue

        # Optional SC relevance filter
        if not is_valid_sc_article(article):
            stats["filtered_non_sc"] += 1
            continue

        # URL duplicate check
        if url in seen_urls:
            stats["url_duplicates"] += 1
            continue

        # Content duplicate check
        content_hash = generate_hash(content)
        if content_hash in seen_content_hashes:
            stats["content_duplicates"] += 1
            continue

        # Title similarity duplicate check
        normalized_title = normalize_title(title)
        duplicate_found = False

        for prev_title in seen_titles[-100:]:
            if is_similar(normalized_title, prev_title, SIMILARITY_THRESHOLD):
                stats["title_similar_duplicates"] += 1
                duplicate_found = True
                break

        if duplicate_found:
            continue

        # Store clean article
        cleaned_article = {
            "url": url,
            "title": title,
            "content": content,
            "date": date
        }

        cleaned_articles.append(cleaned_article)

        seen_urls.add(url)
        seen_content_hashes.add(content_hash)
        seen_titles.append(normalized_title)

    stats["retained"] = len(cleaned_articles)

    return cleaned_articles, stats


# =========================================================
# FILE OPERATIONS
# =========================================================

def load_articles(file_path: Path) -> List[Dict]:
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_articles(file_path: Path, articles: List[Dict]):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)


# =========================================================
# REPORTING
# =========================================================

def print_stats(stats: Dict):
    print("\n===== DEDUPLICATION REPORT =====")
    print(f"Total Articles Scanned        : {stats['total']}")
    print(f"URL Duplicates Removed        : {stats['url_duplicates']}")
    print(f"Content Duplicates Removed    : {stats['content_duplicates']}")
    print(f"Similar Title Duplicates      : {stats['title_similar_duplicates']}")
    print(f"Filtered Non-SC Articles      : {stats['filtered_non_sc']}")
    print(f"Final Retained Articles       : {stats['retained']}")
    print("================================\n")


# =========================================================
# MAIN
# =========================================================

def main():
    print("Loading raw scraper data...")
    raw_articles = load_articles(RAW_FILE)

    print(f"Loaded {len(raw_articles)} raw articles")
    print("Cleaning + deduplicating...")

    cleaned_articles, stats = dedupe_articles(raw_articles)

    print("Saving cleaned dataset...")
    save_articles(OUTPUT_FILE, cleaned_articles)

    print_stats(stats)

    print(f"Cleaned file saved to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()