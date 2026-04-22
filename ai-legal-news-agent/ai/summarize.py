import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from utils.file_utils import get_hash, is_valid, load_json, normalize_text, save_json

logger = logging.getLogger(__name__)

DEFAULT_INPUT_FILE = "data/processed/deduplicated_articles.json"
FALLBACK_INPUT_FILE = "data/processed/clean_articles.json"
DEFAULT_OUTPUT_FILE = "data/processed/processed_articles.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

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
    res = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    res.raise_for_status()
    data = res.json()
    return data.get("response", "") if isinstance(data, dict) else ""


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
        try:
            res = requests.get("http://localhost:11434/api/tags", timeout=2)
            return res.status_code == 200
        except Exception:
            return False


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

    # Resume support: skip already processed URLs/hashes.
    existing = load_json(output_file, default=[])
    done_hashes = {get_hash(x) for x in existing if isinstance(x, dict)}

    unique: List[Dict[str, Any]] = []
    seen = set()
    for a in articles:
        h = get_hash(a)
        if h in seen or h in done_hashes:
            continue
        seen.add(h)
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

