import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Dict, Set
from dataclasses import dataclass
import os
from collections import deque
from functools import lru_cache
import dateutil.parser
import logging
import argparse
from tqdm import tqdm
try:
    import jellyfish
except ImportError:
    jellyfish = None
    logging.warning("jellyfish not installed - fuzzy content dedup disabled")

# =========================================================
# CONFIG
# =========================================================

@dataclass
class Config:
    input_file: str = "../Scraper/Data/Raw_Data/articles.json"
    output_file: str = "Nr_Sc_Articles.json"
    similarity_threshold: float = 0.88
    content_similarity_threshold: float = 0.85
    title_history_limit: int = 5000
    blocked_keywords: list = None

    def __post_init__(self):
        if self.blocked_keywords is None:
            self.blocked_keywords = [
                "weekly digest", "daily round-up", "daily roundup",
                "top stories", "round-up", "weekly roundup",
                "interview", "opinion", "editorial", "podcast"
            ]
        base_dir = Path(__file__).parent.resolve()
        self.input_path = base_dir / self.input_file
        self.output_path = base_dir / self.output_file

CONFIG = Config()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =========================================================
# UTILITIES
# =========================================================

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    return " ".join(text.split()).strip()

def normalize_title(title: str) -> str:
    """Normalize title for duplicate comparison - improved punctuation handling"""
    if not title:
        return ""
    title = title.lower().strip()
    # Remove trailing ellipses/subtitles, but keep basic punctuation
    title = re.sub(r'\.\.\.|:\s*.*$', '', title)
    # Remove extra whitespace/punctuation but keep words separated
    title = re.sub(r'[^a-z0-9\s]', ' ', title)
    title = ' '.join(title.split())
    return title

def generate_hash(text: str) -> str:
    """Generate MD5 hash of text"""
    return hashlib.md5(clean_text(text).encode('utf-8')).hexdigest()

def fuzzy_content_similarity(content1: str, content2: str) -> float:
    """Fuzzy content similarity using jellyfish Jaro-Winkler"""
    if not jellyfish:
        return 0.0
    return jellyfish.jaro_winkler_similarity(content1[:500], content2[:500])  # First 500 chars

def parse_date(date_str: str):
    """Robust date parsing with dateutil fallback"""
    if not date_str:
        return datetime.min
    try:
        # Try ISO first
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        try:
            # Fallback to dateutil
            return dateutil.parser.parse(date_str)
        except:
            logger.warning(f"Date parse failed: {date_str}")
            return datetime.min

def is_valid_sc_article(article: Dict) -> bool:
    """Filter for Supreme Court relevant articles"""
    url = article.get("url", "").lower()
    title = article.get("title", "").lower()
    content = article.get("content", "").lower()

    # Hard reject patterns
    reject_patterns = [
        "/high-court/", "/district-court/", "/tribunal/", "/law-firms/",
        "digest", "live updates", "quarterly digest", "weekly digest",
        "monthly digest", "roundup", "explainer", "podcast", "interview"
    ]
    
    if any(p in url or p in title for p in reject_patterns):
        return False

    # Strong SC indicators
    sc_patterns = [
        "/supreme-court/", "supreme court", "cji", "justice surya kant",
        "constitution bench", "article 32", "sc "
    ]
    
    score = sum(1 for p in sc_patterns if p in url or p in title or p in content[:1500])
    return score >= 2
# =========================================================
# MAIN DEDUPER
# =========================================================

def dedupe_articles(raw_articles: List[Dict]) -> tuple[List[Dict], Dict]:
    """Main deduplication logic with improvements"""
    seen_urls = set()
    seen_content_hashes = set()
    seen_content_fuzzy = set()  # For fuzzy content
    title_history = deque(maxlen=CONFIG.title_history_limit)

    cleaned_articles = []
    stats = {
        "total": 0, "url_duplicates": 0, "content_exact": 0,
        "content_fuzzy": 0, "title_similar": 0,
        "filtered_non_sc": 0, "invalid": 0, "retained": 0
    }

    # Sort by date newest first
    raw_articles.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)

    for article in tqdm(raw_articles, desc="Processing articles"):
        stats["total"] += 1

        url = article.get("url", "").strip()
        title = clean_text(article.get("title", ""))
        content = clean_text(article.get("content", ""))
        date = article.get("date", "")

        if not all([url, title, content]):
            stats["invalid"] += 1
            continue

        # SC filter first
        if not is_valid_sc_article(article):
            stats["filtered_non_sc"] += 1
            continue

        # URL exact duplicate
        if url in seen_urls:
            stats["url_duplicates"] += 1
            continue

        content_hash = generate_hash(content)
        if content_hash in seen_content_hashes:
            stats["content_exact"] += 1
            continue

        # Fuzzy content duplicate
        content_fingerprint = content[:500]  # Truncate for fuzzy
        if jellyfish and content_fingerprint in seen_content_fuzzy:
            stats["content_fuzzy"] += 1
            continue
        if jellyfish:
            seen_content_fuzzy.add(content_fingerprint)

        # Title similarity (LRU-cached)
        normalized_title = normalize_title(title)
        duplicate_found = any(
            SequenceMatcher(None, normalized_title, prev_title).ratio() >= CONFIG.similarity_threshold
            for prev_title in title_history
        )

        if duplicate_found:
            stats["title_similar"] += 1
            continue

        # Accepted
        cleaned_article = {
            "url": url, "title": title, "content": content, "date": date
        }
        cleaned_articles.append(cleaned_article)

        seen_urls.add(url)
        seen_content_hashes.add(content_hash)
        title_history.append(normalized_title)
        stats["retained"] += 1

    return cleaned_articles, stats

# =========================================================
# FILE OPERATIONS
# =========================================================

def load_articles(file_path: Path) -> List[Dict]:
    """Load and validate JSON articles"""
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        if not isinstance(articles, list):
            raise ValueError("Root must be list of articles")
        logger.info(f"Loaded {len(articles)} articles from {file_path}")
        return articles
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise

def save_articles(file_path: Path, articles: List[Dict]):
    """Save articles with pretty JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(articles)} articles to {file_path}")

# =========================================================
# REPORTING
# =========================================================

def print_stats(stats: Dict):
    """Enhanced stats report"""
    print("\n===== DEDUPLICATION REPORT =====")
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title():<25}: {value}")
    print("================================\n")

# =========================================================
# CLI
# =========================================================

def parse_args():
    parser = argparse.ArgumentParser(description="Deduplicate SC articles")
    parser.add_argument('--input', '-i', help="Input JSON path")
    parser.add_argument('--output', '-o', help="Output JSON path")
    parser.add_argument('--threshold', '-t', type=float, help="Similarity threshold")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Override config if CLI args
    if args.input:
        CONFIG.input_file = args.input
        CONFIG.input_path = Path(args.input).resolve()
    if args.output:
        CONFIG.output_file = args.output
        CONFIG.output_path = Path(args.output).resolve()
    if args.threshold:
        CONFIG.similarity_threshold = args.threshold

    logger.info(f"Using input: {CONFIG.input_path}")
    logger.info(f"Using output: {CONFIG.output_path}")

    raw_articles = load_articles(CONFIG.input_path)
    cleaned_articles, stats = dedupe_articles(raw_articles)
    save_articles(CONFIG.output_path, cleaned_articles)
    print_stats(stats)

    logger.info("Deduplication complete!")

if __name__ == "__main__":
    main()
