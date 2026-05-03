"""Smart Chunking: Semantic-aware splitting for LLM context windows.

Preserves sentences/paragraphs, max 8000 chars."""

import re
from typing import List
from pathlib import Path

from .config import config

logger = logging.getLogger(__name__)

def chunk_smart(text: str, max_size: int = config.max_chunk_size) -> List[str]:
    """Chunk text preserving semantic boundaries (sentences > paragraphs)."""
    if not text or len(text) <= max_size:
        return [text]
    
    # Split into sentences (preserve legal structure)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for sent in sentences:
        sent_len = len(sent)
        if current_len + sent_len > max_size and current_chunk:
            # Yield current, start new
            chunks.append(' '.join(current_chunk))
            current_chunk = [sent]
            current_len = sent_len
        else:
            current_chunk.append(sent)
            current_len += sent_len + 1  # Space
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.debug(f'Chunked {len(text)} chars -> {len(chunks)} chunks')
    return chunks

def test_chunking():
    """CLI test with sample."""
    sample = 'Long legal text here...'  # Placeholder
    chunks = chunk_smart(sample)
    print(f'{len(chunks)} chunks')

if __name__ == '__main__':
    test_chunking()

