from __future__ import annotations


def synthesize(title: str, summary: str, citations: list[str]) -> str:
    cite_block = "; ".join(citations[:3]) if citations else "No verified citations available."
    return f"{title}: {summary[:320]} Source grounding: {cite_block}"
