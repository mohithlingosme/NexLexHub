from __future__ import annotations

from nexlexhub.processing.metadata_extractor import extract_metadata


def extract(text: str, title: str) -> dict:
    return extract_metadata(text, title)
