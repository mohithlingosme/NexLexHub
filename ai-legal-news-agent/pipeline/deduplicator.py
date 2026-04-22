import logging
from typing import Any, Dict, List

from utils.file_utils import get_hash, load_json, save_json

logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "data/processed/clean_articles.json"
DEFAULT_OUTPUT_FILE = "data/processed/deduplicated_articles.json"


def deduplicate_articles(
    input_file: str = DEFAULT_INPUT_FILE, output_file: str = DEFAULT_OUTPUT_FILE
) -> List[Dict[str, Any]]:
    articles = load_json(input_file, default=[])
    seen = set()
    deduped: List[Dict[str, Any]] = []
    dropped = 0

    for article in articles:
        if not isinstance(article, dict):
            dropped += 1
            continue
        h = get_hash(article)
        if h in seen:
            dropped += 1
            continue
        seen.add(h)
        deduped.append(article)

    save_json(deduped, output_file)
    logger.info("Deduplicated %d -> %d (dropped %d). Output: %s", len(articles), len(deduped), dropped, output_file)
    return deduped


def main() -> None:
    logger.info("Deduplicating: %s -> %s", DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE)
    deduped = deduplicate_articles()
    logger.info("Dedup done: %d unique articles", len(deduped))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()

