import logging
from utils.file_utils import load_json, save_json, hash_content

logger = logging.getLogger(__name__)

INPUT_FILE = "data/processed/clean_articles.json"
OUTPUT_FILE = "data/processed/deduplicated_articles.json"

def main():
    articles = load_json(INPUT_FILE)
    seen = set()
    deduped = []
    
    for article in articles:
        h = hash_content(article.get("title", ""), article.get("content", ""))
        if h not in seen:
            seen.add(h)
            deduped.append(article)
    
    save_json(deduped, OUTPUT_FILE)
    logger.info(f"Deduplicated: {len(deduped)} unique articles")

if __name__ == "__main__":
    main()

