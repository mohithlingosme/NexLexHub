import json
import logging
from utils.file_utils import load_json, save_json

logger = logging.getLogger(__name__)

INPUT_FILE = "data/raw/articles.json"
CHUNK_SIZE = 500
OUTPUT_DIR = "data/chunks"

def main():
    logger.info("Starting chunking...")
    articles = load_json(INPUT_FILE)
    
    chunk = []
    file_index = 0
    
    for obj in articles:
        chunk.append(obj)
        
        if len(chunk) >= CHUNK_SIZE:
            output_file = f"{OUTPUT_DIR}/chunk_{file_index}.json"
            save_json(chunk, output_file)
            logger.info(f"Saved chunk_{file_index}.json ({len(chunk)} articles)")
            chunk = []
            file_index += 1
    
    # Save remainder
    if chunk:
        output_file = f"{OUTPUT_DIR}/chunk_{file_index}.json"
        save_json(chunk, output_file)
        logger.info(f"Saved final chunk_{file_index}.json ({len(chunk)} articles)")

if __name__ == "__main__":
    main()

