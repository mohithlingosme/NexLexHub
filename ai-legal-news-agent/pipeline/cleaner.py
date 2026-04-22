import logging
import re
from urllib.parse import urlparse
from typing import Any, Dict, List, Optional

from utils.file_utils import load_json, normalize_text, save_json

logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "data/raw/articles.json"
DEFAULT_OUTPUT_FILE = "data/processed/clean_articles.json"

_MCQ_RE = re.compile(r"\b(mcq|multiple\s+choice|question\s*\d+|quiz|exam)\b", re.IGNORECASE)
_OPTION_RE = re.compile(r"(?:^|\n)\s*(?:[A-D]\)|\([A-D]\)|[A-D]\.)\s+\w+", re.IGNORECASE)


def _looks_like_mcq(text: str) -> bool:
    t = text or ""
    if _MCQ_RE.search(t):
        return True
    # Common option formatting: "A) ... B) ... C) ..."
    return len(_OPTION_RE.findall(t)) >= 3


def _is_valid_url(url: str) -> bool:
    u = normalize_text(url)
    if not u:
        return False
    try:
        p = urlparse(u)
    except Exception:
        return False
    return p.scheme in ("http", "https") and bool(p.netloc)


def is_valid_article(article: Dict[str, Any], min_chars: int = 200) -> bool:
    title = normalize_text(article.get("title", ""))
    content = normalize_text(article.get("content", ""))
    url = normalize_text(article.get("url", ""))
    if not title or not content:
        return False
    if len(content) < min_chars:
        return False
    if _looks_like_mcq(content):
        return False
    if url and not _is_valid_url(url):
        return False
    return True


def clean_articles(
    input_file: str = DEFAULT_INPUT_FILE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    min_chars: int = 200,
) -> List[Dict[str, Any]]:
    raw_articles = load_json(input_file, default=[])
    cleaned: List[Dict[str, Any]] = []
    dropped = 0

    for article in raw_articles:
        try:
            if not isinstance(article, dict):
                dropped += 1
                continue
            if not is_valid_article(article, min_chars=min_chars):
                dropped += 1
                continue

            cleaned.append(
                {
                    "title": normalize_text(article.get("title", "")),
                    "content": normalize_text(article.get("content", "")),
                    "date": normalize_text(article.get("date", "")),
                    "url": normalize_text(article.get("url", "")),
                    "category": normalize_text(article.get("category", "")),
                }
            )
        except Exception:
            dropped += 1
            logger.exception("Failed to clean an article; dropping it.")

    save_json(cleaned, output_file)
    logger.info("Cleaned %d articles (dropped %d). Output: %s", len(cleaned), dropped, output_file)
    return cleaned


def main() -> None:
    logger.info("Cleaning: %s -> %s", DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE)
    cleaned = clean_articles()
    logger.info("Cleaning done: %d articles", len(cleaned))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()

