import logging
from typing import Any, Dict, List, Optional, Tuple

from config import DEFAULT_CONFIG
from ai.ollama_client import embed_one as ollama_embed_one
from ai.ollama_client import generate as ollama_generate
from utils.file_utils import load_json, normalize_text
from utils.vector_utils import cosine, hash_embed

logger = logging.getLogger(__name__)

DEFAULT_STORE_FILE = DEFAULT_CONFIG.paths.vector_store

MODEL = DEFAULT_CONFIG.ollama.summarize_model


def _lexical_score(query: str, text: str) -> float:
    q = [t for t in normalize_text(query).lower().split() if t]
    if not q:
        return 0.0
    doc = normalize_text(text).lower()
    score = 0.0
    for tok in set(q):
        # very small, dependency-free BM25-ish signal
        tf = doc.count(tok)
        if tf:
            score += 1.0 + (tf ** 0.5)
    return score


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
    if isinstance(backend, str) and backend.startswith("ollama:"):
        model = backend.split(":", 1)[1] if ":" in backend else DEFAULT_CONFIG.ollama.embed_model
        try:
            qv = ollama_embed_one(q, model=model)
        except Exception:
            logger.warning("Ollama query embedding failed; falling back to lexical retrieval.")
            qv = None

    if qv is None and (not isinstance(backend, str) or backend == "hash"):
        qv = hash_embed(q)

    scored: List[Tuple[float, Dict[str, Any]]] = []
    if qv is not None:
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
    else:
        # Lexical fallback for "ollama:*" stores when Ollama isn't reachable at query-time.
        for it in items:
            if not isinstance(it, dict):
                continue
            meta = it.get("meta")
            if not isinstance(meta, dict):
                continue
            text = str(meta.get("text", "") or "")
            if not text:
                continue
            scored.append((_lexical_score(q, text), meta))

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
        return normalize_text(ollama_generate(prompt, model=MODEL))
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
