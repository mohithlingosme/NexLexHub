import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from config import DEFAULT_CONFIG
from utils.http_utils import get_with_retries, post_json_with_retries
from utils.file_utils import get_hash, is_valid, load_json, normalize_text, save_json

logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = DEFAULT_CONFIG.paths.dedup_articles
FALLBACK_INPUT_FILE = DEFAULT_CONFIG.paths.clean_articles
DEFAULT_OUTPUT_FILE = DEFAULT_CONFIG.paths.processed_articles

OLLAMA_URL = DEFAULT_CONFIG.ollama.generate_url
OLLAMA_TAGS_URL = DEFAULT_CONFIG.ollama.tags_url
MODEL = DEFAULT_CONFIG.ollama.summarize_model

MAX_WORKERS = 3
SAVE_EVERY = 20


def _build_prompt(article: Dict[str, Any]) -> str:
    title = normalize_text(article.get("title", ""))
    content = normalize_text(article.get("content", ""))[:3000]
    return f"""Return ONLY a valid JSON object with these keys.

{{
  "headline": "short engaging headline",
  "intro": "about 100 words",
  "analysis": "about 200 words legal analysis",
  "legal_principles": ["principle 1", "principle 2"],
  "conclusion": "key takeaway"
}}

Article Title: {title}
Content: {content}
"""


def _extract_json(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except Exception:
        return None


def _call_ollama_http(prompt: str) -> str:
    data = post_json_with_retries(
        OLLAMA_URL,
        {"model": MODEL, "prompt": prompt, "stream": False},
        timeout_s=120,
        retries=2,
        base_delay_s=1.2,
    )
    return str(data.get("response", "") or "")


def _call_ollama(prompt: str) -> str:
    """
    Prefer the official `ollama` Python package when available; fall back to the
    HTTP API for environments that only have `requests`.
    """
    try:
        import ollama  # type: ignore

        resp = ollama.generate(model=MODEL, prompt=prompt, stream=False)
        if isinstance(resp, dict):
            return str(resp.get("response", "") or "")
    except Exception:
        pass
    return _call_ollama_http(prompt)


def _ollama_available() -> bool:
    try:
        import ollama  # type: ignore

        resp = ollama.list()
        return isinstance(resp, dict) or isinstance(resp, list)
    except Exception:
        res = get_with_retries(OLLAMA_TAGS_URL, timeout_s=2, retries=1)
        return bool(res is not None and res.status_code == 200)


def _summarize_fallback(article: Dict[str, Any]) -> Dict[str, Any]:
    title = normalize_text(article.get("title", ""))
    content = normalize_text(article.get("content", ""))
    intro = content[:450]
    return {
        "headline": title or "Legal News Update",
        "intro": intro,
        "analysis": "",
        "legal_principles": [],
        "conclusion": "",
    }


def process_article(article: Dict[str, Any], *, use_ollama: bool) -> Dict[str, Any]:
    prompt = _build_prompt(article)
    parsed: Optional[Dict[str, Any]] = None
    source_hash = get_hash(article)

    if use_ollama:
        try:
            raw = _call_ollama(prompt)
            parsed = _extract_json(raw)
        except Exception as exc:
            # Keep pipeline runnable even when Ollama isn't running.
            logger.warning("Ollama unavailable; using fallback summary (%s)", str(exc))

    ai_summary = parsed or _summarize_fallback(article)
    return {
        "title": normalize_text(article.get("title", "")),
        "date": normalize_text(article.get("date", "")),
        "url": normalize_text(article.get("url", "")),
        "source_hash": source_hash,
        "ai_summary": ai_summary,
    }


def summarize_articles(
    input_file: str = DEFAULT_INPUT_FILE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    max_workers: int = MAX_WORKERS,
) -> List[Dict[str, Any]]:
    articles = load_json(input_file, default=[])
    if not articles and input_file != FALLBACK_INPUT_FILE:
        articles = load_json(FALLBACK_INPUT_FILE, default=[])

    articles = [a for a in articles if isinstance(a, dict) and is_valid(a, min_chars=200)]

    # Resume support: skip already processed URLs (preferred) or source_hashes.
    existing = load_json(output_file, default=[])
    done_urls = {normalize_text(x.get("url", "")) for x in existing if isinstance(x, dict) and x.get("url")}
    done_hashes = {normalize_text(x.get("source_hash", "")) for x in existing if isinstance(x, dict) and x.get("source_hash")}

    unique: List[Dict[str, Any]] = []
    seen = set()
    for a in articles:
        url = normalize_text(a.get("url", ""))
        src_hash = get_hash(a)
        if url:
            if url in seen or url in done_urls:
                continue
            seen.add(url)
        else:
            if src_hash in seen or src_hash in done_hashes:
                continue
            seen.add(src_hash)
        unique.append(a)

    processed: List[Dict[str, Any]] = list(existing) if isinstance(existing, list) else []

    use_ollama = _ollama_available()
    if not use_ollama:
        logger.warning("Ollama not reachable; summarization will use a deterministic fallback.")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_article, a, use_ollama=use_ollama) for a in unique]
        for i, fut in enumerate(tqdm(as_completed(futures), total=len(futures), desc="Summarizing")):
            processed.append(fut.result())
            if (i + 1) % SAVE_EVERY == 0:
                save_json(processed, output_file)

    save_json(processed, output_file)
    return processed


def main() -> None:
    logger.info("Summarize: %s -> %s", DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE)
    processed = summarize_articles()
    logger.info("Summarize done: %d items", len(processed))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()

