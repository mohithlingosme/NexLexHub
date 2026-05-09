from __future__ import annotations


def copyright_risk_score(text: str, snippet: str) -> float:
    if not text:
        return 0.0
    overlap = len(set(text.split()) & set(snippet.split()))
    return round(min(1.0, overlap / max(1, len(text.split()) * 0.25)), 3)
