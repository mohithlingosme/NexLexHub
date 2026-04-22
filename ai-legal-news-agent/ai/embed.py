import glob
import logging
from typing import Any, Dict, List, Optional

from tqdm import tqdm

from config import DEFAULT_CONFIG
from ai.ollama_client import embed_many as ollama_embed_many
from utils.file_utils import load_json, normalize_text, resolve_path, save_json
from utils.vector_utils import hash_embed

logger = logging.getLogger(__name__)

DEFAULT_CHUNKS_GLOB = DEFAULT_CONFIG.paths.chunks_glob
DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

DEFAULT_EMBED_MODEL = DEFAULT_CONFIG.ollama.embed_model


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
    resume: bool = True,
) -> str:
    chunks = load_chunks(chunks_glob)
    if not chunks:
        raise FileNotFoundError(f"No chunks found for glob: {chunks_glob}")

    if limit is not None:
        chunks = chunks[: max(0, int(limit))]

    existing = load_json(store_file, default={}) if resume else {}
    existing_backend = existing.get("backend") if isinstance(existing, dict) else None
    existing_items = existing.get("items") if isinstance(existing, dict) else None
    existing_by_id: Dict[str, Dict[str, Any]] = {}
    if isinstance(existing_items, list):
        for it in existing_items:
            if not isinstance(it, dict):
                continue
            meta = it.get("meta")
            vec = it.get("vector")
            if not isinstance(meta, dict) or not isinstance(vec, list):
                continue
            cid = str(meta.get("id") or "")
            if cid:
                existing_by_id[cid] = {"meta": meta, "vector": vec}

    texts_all: List[str] = []
    metas_all: List[Dict[str, Any]] = []
    for c in chunks:
        text = normalize_text(str(c.get("text", "")))
        if not text:
            continue
        cid = str(c.get("id") or "")
        texts_all.append(text)
        metas_all.append(
            {
                "id": cid,
                "url": c.get("url"),
                "title": c.get("title"),
                "date": c.get("date"),
                "chunk_index": c.get("chunk_index"),
                "text": text,
            }
        )

    backend = "hash"
    vectors: List[List[float]] = []

    def _select_missing(target_backend: str) -> tuple[list[str], list[Dict[str, Any]]]:
        if resume and existing_by_id and existing_backend == target_backend:
            texts: List[str] = []
            metas: List[Dict[str, Any]] = []
            for t, m in zip(texts_all, metas_all):
                cid = str(m.get("id") or "")
                if cid and cid in existing_by_id:
                    continue
                texts.append(t)
                metas.append(m)
            return texts, metas
        return list(texts_all), list(metas_all)

    metas: List[Dict[str, Any]] = []
    texts: List[str] = []

    if prefer_ollama:
        backend = f"ollama:{embed_model}"
        texts, metas = _select_missing(backend)
        try:
            vectors = ollama_embed_many(texts, model=embed_model)
        except Exception as exc:
            logger.warning("Ollama embeddings unavailable; falling back to hash embeddings (%s)", str(exc))
            backend = "hash"
            texts, metas = _select_missing(backend)
            vectors = []

    if backend == "hash" and not vectors:
        texts, metas = _select_missing("hash")
        vectors = [hash_embed(t) for t in tqdm(texts, desc="Embedding (hash)")]

    items: List[Dict[str, Any]] = []
    if resume and existing_by_id and existing_backend == backend:
        items.extend(existing_by_id.values())

    items.extend([{"meta": m, "vector": v} for m, v in zip(metas, vectors)])
    payload = {"backend": backend, "items": items}
    save_json(payload, store_file)
    logger.info("Saved vector store (%s): %s", backend, store_file)
    return store_file


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    build_vector_store()


if __name__ == "__main__":
    main()
