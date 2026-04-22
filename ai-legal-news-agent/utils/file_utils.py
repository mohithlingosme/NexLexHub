import hashlib
import json
import logging
import os
from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def project_root() -> Path:
    # ai-legal-news-agent/utils/file_utils.py -> ai-legal-news-agent/
    return Path(__file__).resolve().parents[1]


def resolve_path(path: Union[str, Path]) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return project_root() / p


def ensure_dir(path: Union[str, Path]) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def load_json(file_path: Union[str, Path], default: Optional[Any] = None) -> Any:
    """Load JSON (array/object) or NDJSON. Returns default (or []) when missing."""
    path = resolve_path(file_path)
    if not path.exists():
        if default is not None:
            return default
        logger.warning("File not found: %s", str(path))
        return []

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return default if default is not None else []

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # NDJSON fallback
        items: List[Any] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Skipping invalid NDJSON line in %s", str(path))
        return items


def save_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> None:
    """Save JSON to disk, creating parent directories if needed."""
    path = resolve_path(file_path)
    ensure_dir(path.parent)
    payload = json.dumps(data, indent=indent, ensure_ascii=False)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(path)


def normalize_text(text: str) -> str:
    return " ".join((text or "").split()).strip()


def hash_content(title: str, content: str, truncate: int = 500) -> str:
    """Stable hash for deduplication; truncation limits cost while staying robust."""
    payload = (normalize_text(title) + "\n" + normalize_text(content)[:truncate]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def get_hash(article: Dict[str, Any]) -> str:
    return hash_content(article.get("title", ""), article.get("content", ""))


def is_valid(article: Dict[str, Any], min_chars: int = 1) -> bool:
    title = normalize_text(article.get("title", ""))
    content = normalize_text(article.get("content", ""))
    return bool(title) and len(content) >= min_chars

