from __future__ import annotations

import logging
import math
import re
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from config import DEFAULT_CONFIG
from ai.ollama_client import embed_one as ollama_embed_one
from ai.ollama_client import generate as ollama_generate
from utils.file_utils import load_json, normalize_text, resolve_path
from utils.vector_utils import cosine, hash_embed

logger = logging.getLogger(__name__)

DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

MODEL = DEFAULT_CONFIG.ollama.summarize_model


_WORD_RE = re.compile(r"[a-z0-9]{2,}", re.IGNORECASE)
_STORE_LOCK = threading.Lock()
_STORE_CACHE: Dict[str, Tuple[float, str, List["StoreItem"]]] = {}


@dataclass(frozen=True)
class StoreItem:
    meta: Dict[str, Any]
    vector: Optional[List[float]]
    token_counts: Dict[str, int]


def _tokenize_counts(text: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for tok in _WORD_RE.findall(normalize_text(text).lower()):
        counts[tok] = counts.get(tok, 0) + 1
    return counts


def _load_store_cached(store_file: str) -> Tuple[str, List[StoreItem]]:
    path = resolve_path(store_file)
    if not path.exists():
        raise FileNotFoundError(store_file)

    mtime = path.stat().st_mtime
    key = str(path)
    with _STORE_LOCK:
        cached = _STORE_CACHE.get(key)
        if cached and cached[0] == mtime:
            return cached[1], cached[2]

    store = load_json(store_file, default={})
    backend = store.get("backend") if isinstance(store, dict) else None
    items = store.get("items") if isinstance(store, dict) else None
    if not isinstance(backend, str) or not isinstance(items, list) or not items:
        raise FileNotFoundError(store_file)

    parsed: List[StoreItem] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        meta = it.get("meta")
        vec = it.get("vector")
        if not isinstance(meta, dict):
            continue
        vector: Optional[List[float]] = None
        if isinstance(vec, list) and vec:
            try:
                vector = [float(x) for x in vec]
            except Exception:
                vector = None

        text = f"{meta.get('title','')} {meta.get('text','')}"
        parsed.append(StoreItem(meta=meta, vector=vector, token_counts=_tokenize_counts(text)))

    with _STORE_LOCK:
        _STORE_CACHE[key] = (mtime, backend, parsed)
    return backend, parsed


def store_stats(*, store_file: str = DEFAULT_STORE_FILE) -> Dict[str, Any]:
    backend, items = _load_store_cached(store_file)
    return {"store_file": str(resolve_path(store_file)), "backend": backend, "items": len(items)}


def _lexical_score(query_counts: Dict[str, int], item_counts: Dict[str, int]) -> float:
    score = 0.0
    for tok, qn in query_counts.items():
        dn = item_counts.get(tok, 0)
        if not dn:
            continue
        score += min(qn, dn) * (1.0 + math.log1p(dn))
    return score


def retrieve(
    query: str,
    *,
    k: int = 5,
    store_file: str = DEFAULT_STORE_FILE,
) -> List[Dict[str, Any]]:
    backend, items = _load_store_cached(store_file)

    q = normalize_text(query)
    if not q:
        raise ValueError("Query is empty")
    qv: Optional[List[float]] = None
    if backend.startswith("ollama:"):
        model = backend.split(":", 1)[1] if ":" in backend else DEFAULT_CONFIG.ollama.embed_model
        try:
            qv = ollama_embed_one(q, model=model)
        except Exception:
            logger.warning("Ollama query embedding failed; falling back to lexical retrieval.")
            qv = None

    if qv is None and backend == "hash":
        qv = hash_embed(q)

    scored: List[Tuple[float, Dict[str, Any]]] = []
    if qv is not None:
        for it in items:
            try:
                if not it.vector:
                    continue
                score = cosine(qv, it.vector)
            except Exception:
                continue
            scored.append((score, it.meta))
    else:
        # Lexical fallback for "ollama:*" stores when Ollama isn't reachable at query-time.
        q_counts = _tokenize_counts(q)
        for it in items:
            scored.append((_lexical_score(q_counts, it.token_counts), it.meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[: max(1, int(k))]]


def answer_with_context_meta(query: str, contexts: List[Dict[str, Any]]) -> Tuple[str, bool]:
    ctx_blocks = []
    for c in contexts:
        title = normalize_text(str(c.get("title", "")))
        date = normalize_text(str(c.get("date", "")))
        url = normalize_text(str(c.get("url", "")))
        text = normalize_text(str(c.get("text", "")))[:1200]
        ctx_blocks.append(f"TITLE: {title}\nDATE: {date}\nURL: {url}\nEXCERPT: {text}")

    prompt = f"""You are a legal news assistant.
Use ONLY the context excerpts to answer. If context is insufficient, say so.
After your answer, include a short 'Sources' list with title + URL.

Context excerpts:
{chr(10).join(ctx_blocks)}

User question: {normalize_text(query)}
"""

    try:
        return normalize_text(ollama_generate(prompt, model=MODEL)), True
    except Exception as exc:
        logger.warning("Ollama unavailable, returning retrieved excerpts only (%s)", str(exc))
        lines = []
        for c in contexts:
            title = normalize_text(str(c.get("title", "")))
            url = normalize_text(str(c.get("url", "")))
            excerpt = normalize_text(str(c.get("text", "")))[:200]
            lines.append(f"- {title} ({url}): {excerpt}")
        return "Relevant excerpts:\n" + "\n".join(lines), False


def answer_with_context(query: str, contexts: List[Dict[str, Any]]) -> str:
    return answer_with_context_meta(query, contexts)[0]


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    q = "What did the Supreme Court say about arbitration?"
    ctx = retrieve(q, k=5)
    print(answer_with_context(q, ctx))


if __name__ == "__main__":
    main()
