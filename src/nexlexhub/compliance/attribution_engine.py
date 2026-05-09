from __future__ import annotations


def build_attribution(source_url: str, publisher: str, official_source_url: str | None) -> dict[str, str | None]:
    return {
        "publisher": publisher,
        "publisher_url": source_url,
        "official_source_url": official_source_url,
        "policy": "Always cite publisher and prioritize the official source.",
    }
