import json
import os
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def ensure_dir(path: str) -> None:
    """Create directory if not exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Load JSON file (handles both array and NDJSON)."""
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Try NDJSON
            return [json.loads(line.strip()) for line in f if line.strip()]
    
    logger.info(f"Loaded {len(data)} articles from {file_path}")
    return data

def save_json(data: List[Dict], file_path: str, indent: int = 2) -> None:
    """Save list to JSON file."""
    ensure_dir(os.path.dirname(file_path) or '.')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.info(f"Saved {len(data)} articles to {file_path}")

def hash_content(title: str, content: str, truncate: int = 200) -> str:
    """MD5 hash for deduplication."""
    import hashlib
    text = title + content[:truncate]
    return hashlib.md5(text.encode()).hexdigest()

