from __future__ import annotations


def rerank(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda item: (item.get("score", 0), item.get("verified", False)), reverse=True)
