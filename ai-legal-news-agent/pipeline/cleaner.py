import re
import logging
from utils.file_utils import load_json, save_json, hash_content, ensure_dir
from utils.date_parser import parse_date

logger = logging.getLogger(__name__)

INPUT_FILE = "data/raw/articles.json"
OUTPUT_FILE = "data/processed/clean_articles.json"

def is_valid(article):
    \"\"\"Validate article has essential fields and quality checks.\"\"\"
    title = article.get("title", "")
    content = article.get("content", "")
    date = article.get("date", "")
    
    if not title or not content or not date:
        return False
    
    # Skip tiny articles
    if len(content) < 200:
        return False
    
    # Skip MCQ/exam junk
    if any(word in content.lower() for word in ["question", "mcq", "exam"]):
        return False
    
    return True

def main():
    logger.info("Starting cleaning...")
    raw_articles = load_json(INPUT_FILE)
    
    cleaned = []
    seen_hashes = set()
    
    for article in raw_articles:
        if not is_valid(article):
            continue
        
        # Dedup
        h = hash_content(article.get("title", ""), article.get("content", ""))
        if h in seen_hashes:
            continue
        
        seen_hashes.add(h)
        
        cleaned_article = {
            "title": article["title"].strip(),
            "content": article["content"].strip(),
            "date": article.get("date", ""),
            "url": article.get("url", "")
        }
        cleaned.append(cleaned_article)
    
    save_json(cleaned, OUTPUT_FILE)
    logger.info(f"Cleaned {len(cleaned)} articles")

if __name__ == "__main__":
    main()

