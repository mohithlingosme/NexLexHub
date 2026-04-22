import glob
import logging
from typing import Any, Dict, List, Optional, Sequence

from tqdm import tqdm

from config import DEFAULT_CONFIG
from utils.http_utils import post_json_with_retries
from utils.file_utils import load_json, normalize_text, resolve_path, save_json
from utils.vector_utils import hash_embed

logger = logging.getLogger(__name__)

DEFAULT_CHUNKS_GLOB = DEFAULT_CONFIG.paths.chunks_glob
DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

OLLAMA_EMBED_URL = DEFAULT_CONFIG.ollama.embeddings_url
DEFAULT_EMBED_MODEL = DEFAULT_CONFIG.ollama.embed_model


def _ollama_embed_http(texts: Sequence[str], *, model: str) -> List[List[float]]:
    out: List[List[float]] = []
    for t in texts:
        data = post_json_with_retries(
            OLLAMA_EMBED_URL,
            {"model": model, "prompt": t},
            timeout_s=120,
            retries=2,
            base_delay_s=1.2,
        )
        emb = data.get("embedding") if isinstance(data, dict) else None
        if not isinstance(emb, list) or not emb:
            raise RuntimeError("Unexpected Ollama embedding response")
        out.append([float(x) for x in emb])
    return out


def _ollama_embed(texts: Sequence[str], *, model: str) -> Optional[List[List[float]]]:
    try:
        import ollama  # type: ignore

        out: List[List[float]] = []
        for t in texts:
            resp = ollama.embeddings(model=model, prompt=t)
            if not isinstance(resp, dict) or "embedding" not in resp:
                return None
            emb = resp.get("embedding")
            if not isinstance(emb, list) or not emb:
                return None
            out.append([float(x) for x in emb])
        return out
    except Exception:
        return None


def load_chunks(chunks_glob: str = DEFAULT_CHUNKS_GLOB) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    for path in sorted(glob.glob(str(resolve_path(chunks_glob)))):
        data = load_json(path, default=[])
        if isinstance(data, list):
            chunks.extend([x for x in data if isinstance(x, dict)])
    return chunks


def build_vector_store(
    *,
    chunks_glob: str = DEFAULT_CHUNKS_GLOB,
    store_file: str = DEFAULT_STORE_FILE,
    embed_model: str = DEFAULT_EMBED_MODEL,
    prefer_ollama: bool = True,
    limit: Optional[int] = None,
) -> str:
    chunks = load_chunks(chunks_glob)
    if not chunks:
        raise FileNotFoundError(f"No chunks found for glob: {chunks_glob}")

    if limit is not None:
        chunks = chunks[: max(0, int(limit))]

    texts: List[str] = []
    metas: List[Dict[str, Any]] = []
    for c in chunks:
        text = normalize_text(str(c.get("text", "")))
        if not text:
            continue
        texts.append(text)
        metas.append(
            {
                "id": c.get("id"),
                "url": c.get("url"),
                "title": c.get("title"),
                "date": c.get("date"),
                "chunk_index": c.get("chunk_index"),
                "text": text,
            }
        )

    vectors: List[List[float]] = []
    backend = "hash"
    if prefer_ollama:
        oll = _ollama_embed(texts, model=embed_model)
        if oll is not None:
            vectors = oll
            backend = f"ollama:{embed_model}"
        else:
            try:
                vectors = _ollama_embed_http(texts, model=embed_model)
                backend = f"ollama_http:{embed_model}"
            except Exception as exc:
                logger.warning("Ollama embeddings unavailable; falling back to hash embeddings (%s)", str(exc))

    if not vectors:
        vectors = [hash_embed(t) for t in tqdm(texts, desc="Embedding (hash)")]

    payload = {"backend": backend, "items": [{"meta": m, "vector": v} for m, v in zip(metas, vectors)]}
    save_json(payload, store_file)
    logger.info("Saved vector store (%s): %s", backend, store_file)
    return store_file


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    build_vector_store()


if __name__ == "__main__":
    main()
