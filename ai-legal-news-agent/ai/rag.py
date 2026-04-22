import logging
from typing import Any, Dict, List, Optional, Tuple

import requests

from config import DEFAULT_CONFIG
from utils.http_utils import post_json_with_retries
from utils.file_utils import load_json, normalize_text
from utils.vector_utils import cosine, hash_embed

logger = logging.getLogger(__name__)

DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

OLLAMA_URL = DEFAULT_CONFIG.ollama.generate_url
OLLAMA_EMBED_URL = DEFAULT_CONFIG.ollama.embeddings_url
MODEL = DEFAULT_CONFIG.ollama.summarize_model


def _ollama_embed_query(text: str, *, model: str) -> Optional[List[float]]:
    try:
        import ollama  # type: ignore

        resp = ollama.embeddings(model=model, prompt=text)
        if isinstance(resp, dict) and isinstance(resp.get("embedding"), list):
            return [float(x) for x in resp["embedding"]]
    except Exception:
        pass
    return None


def _ollama_embed_query_http(text: str, *, model: str) -> Optional[List[float]]:
    try:
        data = post_json_with_retries(
            OLLAMA_EMBED_URL,
            {"model": model, "prompt": text},
            timeout_s=120,
            retries=2,
            base_delay_s=1.2,
        )
        emb = data.get("embedding") if isinstance(data, dict) else None
        if isinstance(emb, list) and emb:
            return [float(x) for x in emb]
    except Exception:
        return None
    return None


def retrieve(
    query: str,
    *,
    k: int = 5,
    store_file: str = DEFAULT_STORE_FILE,
) -> List[Dict[str, Any]]:
    store = load_json(store_file, default={})
    items = store.get("items") if isinstance(store, dict) else None
    backend = store.get("backend") if isinstance(store, dict) else None
    if not isinstance(items, list) or not items:
        raise FileNotFoundError(store_file)

    q = normalize_text(query)
    qv: Optional[List[float]] = None
    if isinstance(backend, str) and (backend.startswith("ollama:") or backend.startswith("ollama_http:")):
        model = backend.split(":", 1)[1] if ":" in backend else DEFAULT_CONFIG.ollama.embed_model
        qv = _ollama_embed_query(q, model=model) or _ollama_embed_query_http(q, model=model)

    if qv is None:
        qv = hash_embed(q)

    scored: List[Tuple[float, Dict[str, Any]]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        meta = it.get("meta")
        vec = it.get("vector")
        if not isinstance(meta, dict) or not isinstance(vec, list):
            continue
        try:
            score = cosine(qv, [float(x) for x in vec])
        except Exception:
            continue
        scored.append((score, meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[: max(1, int(k))]]


def answer_with_context(query: str, contexts: List[Dict[str, Any]]) -> str:
    ctx_blocks = []
    for c in contexts:
        title = normalize_text(str(c.get("title", "")))
        url = normalize_text(str(c.get("url", "")))
        text = normalize_text(str(c.get("text", "")))[:1200]
        ctx_blocks.append(f"TITLE: {title}\nURL: {url}\nEXCERPT: {text}")

    prompt = f"""You are a legal news assistant.
Use ONLY the context excerpts to answer. If context is insufficient, say so.

Context excerpts:
{chr(10).join(ctx_blocks)}

User question: {normalize_text(query)}
"""

    try:
        data = post_json_with_retries(
            OLLAMA_URL,
            {"model": MODEL, "prompt": prompt, "stream": False},
            timeout_s=120,
            retries=2,
            base_delay_s=1.2,
        )
        return normalize_text(str(data.get("response", "") or ""))
    except Exception as exc:
        logger.warning("Ollama unavailable, returning retrieved excerpts only (%s)", str(exc))
        lines = []
        for c in contexts:
            lines.append(f"- {normalize_text(str(c.get('title','')))} ({normalize_text(str(c.get('url','')))}): {normalize_text(str(c.get('text','')) )[:200]}")
        return "Relevant excerpts:\n" + "\n".join(lines)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    q = "What did the Supreme Court say about arbitration?"
    ctx = retrieve(q, k=5)
    print(answer_with_context(q, ctx))


if __name__ == "__main__":
    main()
