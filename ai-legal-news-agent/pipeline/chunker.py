import logging
from typing import Any, Dict, Iterable, List

from config import DEFAULT_CONFIG
from utils.file_utils import hash_content, load_json, normalize_text, resolve_path, save_json

logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = DEFAULT_CONFIG.paths.dedup_articles
DEFAULT_OUTPUT_DIR = DEFAULT_CONFIG.paths.chunks_dir

DEFAULT_MAX_CHARS = DEFAULT_CONFIG.chunker.max_chars
DEFAULT_OVERLAP = DEFAULT_CONFIG.chunker.overlap
DEFAULT_CHUNKS_PER_FILE = DEFAULT_CONFIG.chunker.chunks_per_file
DEFAULT_PURGE_EXISTING = DEFAULT_CONFIG.chunker.purge_existing


def _chunk_text(text: str, max_chars: int, overlap: int) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []

    # Deterministic chunking that prefers splitting on word boundaries.
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + max_chars)
        if end < n:
            # Avoid chopping a word in half.
            ws = text.rfind(" ", start, end)
            if ws > start + int(max_chars * 0.6):
                end = ws

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks


def build_chunks(
    articles: Iterable[Dict[str, Any]],
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap: int = DEFAULT_OVERLAP,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for article in articles:
        if not isinstance(article, dict):
            continue
        title = normalize_text(article.get("title", ""))
        content = normalize_text(article.get("content", ""))
        if not title or not content:
            continue

        url = normalize_text(article.get("url", ""))
        date = normalize_text(article.get("date", ""))

        pieces = _chunk_text(content, max_chars=max_chars, overlap=overlap)
        for idx, piece in enumerate(pieces):
            chunk_id = hash_content(url or title, f"{idx}:{piece}", truncate=max_chars)
            out.append(
                {
                    "id": chunk_id,
                    "url": url,
                    "title": title,
                    "date": date,
                    "chunk_index": idx,
                    "text": piece,
                }
            )
    return out


def save_chunks(
    chunks: List[Dict[str, Any]],
    output_dir: str = DEFAULT_OUTPUT_DIR,
    chunks_per_file: int = DEFAULT_CHUNKS_PER_FILE,
    purge_existing: bool = DEFAULT_PURGE_EXISTING,
) -> List[str]:
    if purge_existing:
        out_dir = resolve_path(output_dir)
        if out_dir.exists():
            for p in out_dir.glob("chunk_*.json"):
                try:
                    p.unlink()
                except Exception:
                    logger.warning("Failed to delete old chunk file: %s", str(p))

    paths: List[str] = []
    file_index = 0
    batch: List[Dict[str, Any]] = []

    for item in chunks:
        batch.append(item)
        if len(batch) >= chunks_per_file:
            path = f"{output_dir}/chunk_{file_index}.json"
            save_json(batch, path)
            paths.append(path)
            batch = []
            file_index += 1

    if batch:
        path = f"{output_dir}/chunk_{file_index}.json"
        save_json(batch, path)
        paths.append(path)

    return paths


def chunk_articles(
    input_file: str = DEFAULT_INPUT_FILE,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap: int = DEFAULT_OVERLAP,
    chunks_per_file: int = DEFAULT_CHUNKS_PER_FILE,
    purge_existing: bool = DEFAULT_PURGE_EXISTING,
) -> List[str]:
    articles = load_json(input_file, default=[])
    chunks = build_chunks(articles, max_chars=max_chars, overlap=overlap)
    paths = save_chunks(
        chunks,
        output_dir=output_dir,
        chunks_per_file=chunks_per_file,
        purge_existing=purge_existing,
    )
    logger.info(
        "Chunked %d articles into %d chunks (%d files). Output dir: %s",
        len(articles) if isinstance(articles, list) else 0,
        len(chunks),
        len(paths),
        output_dir,
    )
    return paths


def main() -> None:
    logger.info("Chunking: %s -> %s", DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_DIR)
    paths = chunk_articles()
    logger.info("Chunking done: %d files", len(paths))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()

