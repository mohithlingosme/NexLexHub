from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)


def extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """
    Best-effort extraction of the first JSON object from model output.

    Handles:
    - raw JSON with leading/trailing chatter
    - fenced blocks ```json ... ```
    - minor "explanation then JSON" formats
    """
    if not text:
        return None

    candidates = []
    m = _FENCE_RE.search(text)
    if m and m.group(1).strip():
        candidates.append(m.group(1).strip())
    candidates.append(text)

    for cand in candidates:
        start = cand.find("{")
        if start < 0:
            continue

        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(cand)):
            ch = cand[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue

            if ch == '"':
                in_string = True
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    raw = cand[start : i + 1]
                    try:
                        obj = json.loads(raw)
                    except Exception:
                        break
                    return obj if isinstance(obj, dict) else None

    logger.debug("No JSON object found in text (len=%d).", len(text))
    return None

