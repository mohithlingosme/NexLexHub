from __future__ import annotations

import logging
import math
import os
import re
import threading
from dataclasses import dataclass
import hashlib
from types import MappingProxyType
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple

from config import DEFAULT_CONFIG
from ai.ollama_client import embed_one as ollama_embed_one
from ai.ollama_client import generate as ollama_generate
from utils.file_utils import load_json, normalize_text, resolve_path
from utils.vector_utils import cosine, hash_embed, l2_normalize

logger = logging.getLogger(__name__)

DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

MODEL = DEFAULT_CONFIG.ollama.summarize_model


_WORD_RE = re.compile(r"[a-z0-9]{2,}", re.IGNORECASE)
_STORE_LOCK = threading.Lock()
_STORE_CACHE: "OrderedDict[str, Tuple[float, int, str, Tuple['StoreItem', ...]]]" = OrderedDict()
_STORE_CACHE_MAX = 4


def _clamp01(x: float, default: float) -> float:
    try:
        v = float(x)
    except Exception:
        return default
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


RAG_WEIGHT_COSINE = _clamp01(os.getenv("RAG_WEIGHT_COSINE", "0.85"), 0.85)
RAG_WEIGHT_LEXICAL = 1.0 - RAG_WEIGHT_COSINE


@dataclass(frozen=True)
class StoreItem:
    meta: Dict[str, Any]
    vector: Optional[Tuple[float, ...]]
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

    stat = path.stat()
    mtime = stat.st_mtime
    size = int(getattr(stat, "st_size", 0) or 0)
    key = str(path)
    with _STORE_LOCK:
        cached = _STORE_CACHE.get(key)
        if cached and cached[0] == mtime and cached[1] == size:
            # LRU touch
            _STORE_CACHE.move_to_end(key)
            return cached[2], list(cached[3])

    store = load_json(store_file, default={})
    backend = store.get("backend") if isinstance(store, dict) else None
    items = store.get("items") if isinstance(store, dict) else None
    if not isinstance(backend, str) or not isinstance(items, list) or not items:
        raise ValueError(f"Vector store is missing/corrupt: {store_file}")

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
        token_counts = MappingProxyType(_tokenize_counts(text))  # immutable view
        parsed.append(
            StoreItem(
                meta=dict(meta),
                vector=tuple(l2_normalize(vector)) if vector else None,
                token_counts=token_counts,  # type: ignore[arg-type]
            )
        )

    with _STORE_LOCK:
        _STORE_CACHE[key] = (mtime, size, backend, tuple(parsed))
        _STORE_CACHE.move_to_end(key)
        while len(_STORE_CACHE) > _STORE_CACHE_MAX:
            _STORE_CACHE.popitem(last=False)
    return backend, parsed


def store_stats(*, store_file: str = DEFAULT_STORE_FILE) -> Dict[str, Any]:
    backend, items = _load_store_cached(store_file)
    dim = 0
    for it in items:
        if it.vector:
            dim = len(it.vector)
            break
    return {"store_file": str(resolve_path(store_file)), "backend": backend, "items": len(items), "dim": dim}


def _lexical_score(query_counts: Dict[str, int], item_counts: Dict[str, int]) -> float:
    score = 0.0
    for tok, qn in query_counts.items():
        dn = item_counts.get(tok, 0)
        if not dn:
            continue
        score += min(qn, dn) * (1.0 + math.log1p(dn))
    return score


def _hybrid_score(cosine_score: Optional[float], lexical_score: float, *, max_lexical: float, w_cos: float, w_lex: float) -> float:
    lex01 = (lexical_score / max_lexical) if max_lexical > 0 else 0.0
    if cosine_score is None:
        return w_lex * lex01
    cos01 = (cosine_score + 1.0) / 2.0  # [-1,1] -> [0,1]
    return (w_cos * cos01) + (w_lex * lex01)


def _select_contexts(scored: List[Tuple[float, Dict[str, Any]]], *, k: int, max_per_url: int = 2) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    per_url: Dict[str, int] = {}
    seen_chunk_ids: set[str] = set()
    seen_text_hash: set[str] = set()

    for _, meta in scored:
        url = normalize_text(str(meta.get("url", "")))
        cid = normalize_text(str(meta.get("id", "")))
        text = normalize_text(str(meta.get("text", "")))
        if cid and cid in seen_chunk_ids:
            continue
        if text:
            th = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if th in seen_text_hash:
                continue
            seen_text_hash.add(th)

        if url:
            n = per_url.get(url, 0)
            if n >= max_per_url:
                continue
            per_url[url] = n + 1

        if cid:
            seen_chunk_ids.add(cid)
        out.append(dict(meta))
        if len(out) >= k:
            break

    return out


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
            qv = l2_normalize(ollama_embed_one(q, model=model))
        except Exception:
            logger.warning("Ollama query embedding failed; falling back to lexical retrieval.")
            qv = None

    if qv is None and backend == "hash":
        qv = hash_embed(q)

    q_counts = _tokenize_counts(q)
    max_lex = 0.0
    lex_scores: List[float] = []
    for it in items:
        s = _lexical_score(q_counts, it.token_counts)  # type: ignore[arg-type]
        lex_scores.append(s)
        if s > max_lex:
            max_lex = s

    scored: List[Tuple[float, Dict[str, Any]]] = []
    w_cos = RAG_WEIGHT_COSINE
    w_lex = RAG_WEIGHT_LEXICAL

    if qv is not None:
        for it, lex in zip(items, lex_scores):
            cos = None
            if it.vector:
                try:
                    cos = cosine(qv, it.vector)
                except Exception:
                    cos = None
            score = _hybrid_score(cos, lex, max_lexical=max_lex, w_cos=w_cos, w_lex=w_lex)
            scored.append((score, it.meta))
    else:
        for it, lex in zip(items, lex_scores):
            score = _hybrid_score(None, lex, max_lexical=max_lex, w_cos=0.0, w_lex=1.0)
            scored.append((score, it.meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    return _select_contexts(scored, k=max(1, int(k)))


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
