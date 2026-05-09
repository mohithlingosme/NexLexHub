from __future__ import annotations

import re


CITATION_PATTERNS = {
    "scc": re.compile(r"\(\d{4}\)\s*\d+\s*SCC\s*\d+", re.I),
    "air": re.compile(r"AIR\s+\d{4}\s+[A-Z]+\s+\d+", re.I),
    "livelaw": re.compile(r"\d{4}\s+LiveLaw\s+\([A-Z]+\)\s+\d+", re.I),
    "statute": re.compile(r"Section\s+\d+[A-Z]?\s+of\s+the\s+[A-Za-z ,().-]+(?:Act|Code)", re.I),
}


def extract_citations(text: str) -> list[dict[str, str]]:
    citations: list[dict[str, str]] = []
    for citation_type, pattern in CITATION_PATTERNS.items():
        for match in pattern.finditer(text):
            raw = match.group(0).strip()
            citations.append(
                {
                    "raw_text": raw,
                    "normalized_text": re.sub(r"\s+", " ", raw).strip(),
                    "citation_type": citation_type,
                }
            )
    return citations
