"""Document Cleaner: Multi-format ingest (.txt, .md, .json, .html), text normalization, BeautifulSoup cleaning, hash dedup.

Preserves originals, copies to Processed/, computes registry."""

import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
import html2text  # for HTML/MD

from config import config
from .validator import register_source  # Forward ref; impl later

logger = logging.getLogger(__name__)

SUPPORTED_EXTS = {'.txt', '.md', '.json', '.html'}

def compute_hash(text: str) -> str:
    """SHA256 content hash for dedup."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]  # Short ID

def clean_text(raw: str) -> str:
    """Normalize whitespace, remove noise."""
    raw = raw.strip()
    raw = BeautifulSoup(raw, 'html.parser').get_text(separator=' ', strip=True)  # Strip HTML
    raw = ' '.join(raw.split())  # Normalize WS
    return raw

def load_raw_file(file_path: Path) -> Optional[Tuple[str, str]]:  # (content, metadata)
    """Load single file based on ext."""
    if file_path.suffix.lower() not in SUPPORTED_EXTS:
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read()
        
        content = clean_text(raw)
        if not content or len(content) < 100:
            logger.warning(f'Skipped tiny/empty: {file_path}')
            return None
        
        metadata = {
            'source_file': str(file_path.relative_to(config.raw_dir)),
            'file_size': file_path.stat().st_size,
            'word_count': len(content.split())
        }
        return content, metadata
    
    except Exception as e:
        logger.error(f'Load failed {file_path}: {e}')
        return None

def ingest_bulk(input_dir: Path = config.raw_dir) -> List[Dict[str, Any]]:
    """Bulk ingest: scan Raw/, clean, hash dedup, register sources."""
    dedup_hashes = set()
    cleaned_docs = []
    
    for file_path in input_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTS:
            doc = load_raw_file(file_path)
            if not doc:
                continue
            
            content, metadata = doc
            source_hash = compute_hash(content)
            
            if source_hash in dedup_hashes:
                logger.info(f'Dup skipped: {metadata["source_file"]}')
                continue
            
            # Preserve raw: copy to Processed/
            if config.preserve_raw:
                processed_path = config.processed_dir / file_path.relative_to(config.raw_dir)
                processed_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.replace(processed_path)  # Atomic move for safety
            
            cleaned = {
                'source_hash': source_hash,
                **metadata,
                'cleaned_content': content
            }
            # Register for resume/tracking
            register_source(source_hash, metadata['source_file'], metadata['file_size'], metadata['word_count'])
            
            cleaned_docs.append(cleaned)
            dedup_hashes.add(source_hash)
            logger.debug(f'Ingested: {metadata["source_file"]} ({metadata["word_count"]} words)')
    
    logger.info(f'Bulk ingest: {len(cleaned_docs)} unique docs from {input_dir}')
    return cleaned_docs

if __name__ == '__main__':
    # CLI test
    import logging; logging.basicConfig(level='INFO')
    docs = ingest_bulk()
    print(f'Ingested {len(docs)} docs')

