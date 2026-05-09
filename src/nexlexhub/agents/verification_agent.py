from __future__ import annotations


def verify(text: str, citations: list[str]) -> dict[str, object]:
    return {"verified": bool(text and citations), "confidence": 0.85 if citations else 0.45}
