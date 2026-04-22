from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


def post_json_with_retries(
    url: str,
    payload: Dict[str, Any],
    *,
    timeout_s: int = 120,
    retries: int = 3,
    base_delay_s: float = 1.5,
) -> Dict[str, Any]:
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=timeout_s)
            res.raise_for_status()
            data = res.json()
            if not isinstance(data, dict):
                raise ValueError("Expected JSON object response")
            return data
        except Exception as exc:
            last_exc = exc
            delay = base_delay_s * (2**attempt)
            logger.warning("POST retry %d/%d failed: %s (%s)", attempt + 1, retries, url, str(exc))
            time.sleep(delay)
    raise RuntimeError(f"POST failed after {retries} retries: {url}") from last_exc


def get_with_retries(
    url: str,
    *,
    timeout_s: int = 5,
    retries: int = 2,
    base_delay_s: float = 1.0,
) -> Optional[requests.Response]:
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            res = requests.get(url, timeout=timeout_s)
            return res
        except Exception as exc:
            last_exc = exc
            delay = base_delay_s * (2**attempt)
            logger.warning("GET retry %d/%d failed: %s (%s)", attempt + 1, retries, url, str(exc))
            time.sleep(delay)
    logger.warning("GET failed after %d retries: %s (%s)", retries, url, str(last_exc))
    return None
