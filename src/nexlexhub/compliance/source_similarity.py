from __future__ import annotations

from difflib import SequenceMatcher


def similarity_score(a: str, b: str) -> float:
    return round(SequenceMatcher(None, a or "", b or "").ratio(), 3)
