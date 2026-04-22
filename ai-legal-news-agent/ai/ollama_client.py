from __future__ import annotations

import logging
import random
import time
from typing import List, Optional, Sequence

from config import DEFAULT_CONFIG
from utils.http_utils import get_with_retries, post_json_with_retries

logger = logging.getLogger(__name__)


def _import_ollama():
    try:
        import ollama  # type: ignore

        return ollama
    except ModuleNotFoundError:
        return None


def _sleep_backoff(base_delay_s: float, attempt: int) -> None:
    # Jittered exponential backoff (caps jitter to keep it predictable).
    delay = base_delay_s * (2**attempt)
    delay = delay * (0.75 + random.random() * 0.5)
    time.sleep(min(delay, 30.0))


def available(
    *,
    base_url: str = DEFAULT_CONFIG.ollama.base_url,
    timeout_s: int = 2,
    retries: int = 1,
) -> bool:
    """
    Returns True if Ollama is reachable either via the Python package or HTTP.
    """
    ollama = _import_ollama()
    if ollama is not None:
        try:
            resp = ollama.list()
            return isinstance(resp, dict) or isinstance(resp, list)
        except Exception:
            pass

    try:
        res = get_with_retries(f"{base_url}/api/tags", timeout_s=timeout_s, retries=retries)
        return bool(res is not None and res.status_code == 200)
    except Exception:
        return False


def generate(
    prompt: str,
    *,
    model: str = DEFAULT_CONFIG.ollama.summarize_model,
    base_url: str = DEFAULT_CONFIG.ollama.base_url,
    timeout_s: int = 120,
    retries: int = 2,
    base_delay_s: float = 1.2,
) -> str:
    """
    Generate text using Ollama.
    Prefers the `ollama` Python package; falls back to HTTP.
    """
    last_exc: Optional[BaseException] = None
    ollama = _import_ollama()
    if ollama is not None:
        for attempt in range(max(1, int(retries))):
            try:
                resp = ollama.generate(model=model, prompt=prompt, stream=False)
                if isinstance(resp, dict):
                    return str(resp.get("response", "") or "")
                return str(resp or "")
            except Exception as exc:
                last_exc = exc
                _sleep_backoff(base_delay_s, attempt)

    data = post_json_with_retries(
        f"{base_url}/api/generate",
        {"model": model, "prompt": prompt, "stream": False},
        timeout_s=timeout_s,
        retries=retries,
        base_delay_s=base_delay_s,
    )
    return str(data.get("response", "") or "")


def embed_one(
    text: str,
    *,
    model: str = DEFAULT_CONFIG.ollama.embed_model,
    base_url: str = DEFAULT_CONFIG.ollama.base_url,
    timeout_s: int = 120,
    retries: int = 2,
    base_delay_s: float = 1.2,
) -> List[float]:
    """
    Returns a single embedding vector.
    """
    last_exc: Optional[BaseException] = None
    ollama = _import_ollama()
    if ollama is not None:
        for attempt in range(max(1, int(retries))):
            try:
                resp = ollama.embeddings(model=model, prompt=text)
                emb = resp.get("embedding") if isinstance(resp, dict) else None
                if not isinstance(emb, list) or not emb:
                    raise RuntimeError("Unexpected Ollama embedding response")
                return [float(x) for x in emb]
            except Exception as exc:
                last_exc = exc
                _sleep_backoff(base_delay_s, attempt)

    data = post_json_with_retries(
        f"{base_url}/api/embeddings",
        {"model": model, "prompt": text},
        timeout_s=timeout_s,
        retries=retries,
        base_delay_s=base_delay_s,
    )
    emb = data.get("embedding") if isinstance(data, dict) else None
    if not isinstance(emb, list) or not emb:
        raise RuntimeError("Unexpected Ollama embedding response") from last_exc
    return [float(x) for x in emb]


def embed_many(
    texts: Sequence[str],
    *,
    model: str = DEFAULT_CONFIG.ollama.embed_model,
    base_url: str = DEFAULT_CONFIG.ollama.base_url,
    timeout_s: int = 120,
    retries: int = 2,
    base_delay_s: float = 1.2,
) -> List[List[float]]:
    """
    Embeds texts sequentially (safe default for local Ollama).
    """
    out: List[List[float]] = []
    for t in texts:
        out.append(
            embed_one(
                t,
                model=model,
                base_url=base_url,
                timeout_s=timeout_s,
                retries=retries,
                base_delay_s=base_delay_s,
            )
        )
    return out
