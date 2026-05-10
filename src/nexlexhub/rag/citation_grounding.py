from __future__ import annotations

import re
from typing import Any

from nexlexhub.processing.citation_extractor import extract_citations


_CITATION_INLINE_RE = re.compile(
    r"(\((?:19|20)\d{2}\)\s*\d+\s*SCC\s*\d+|AIR\s+(?:19|20)\d{2}\s+[A-Z]+\s+\d+)"
    ,
    re.IGNORECASE,
)


def _extract_sources(text: str) -> list[str]:
    """Return inline citation-like strings present in a text."""
    return [m.group(1).strip() for m in _CITATION_INLINE_RE.finditer(text or "")]


def _extract_statute_refs(text: str) -> list[str]:
    # extract_citations already classifies "statute" vs precedents
    cit = extract_citations(text or "")
    return [c["raw_text"] for c in cit if c.get("citation_type") == "statute"]


def ground_answer(answer: str, citations: list[str], *, retrieved_chunks: list[dict] | None = None) -> dict[str, Any]:
    """Production-friendly grounding stub.

    Requirements (current phase):
    - include paragraph refs + page refs + source citations + chunk references
    - include official source links (best-effort from retrieved_chunks)

    NOTE: full SCC/AIR parsing + exact paragraph matching will be added in the next iteration.
    """

    retrieved_chunks = retrieved_chunks or []

    # chunk ids we used (best-effort)
    chunk_refs = [c.get("chunk_id") for c in retrieved_chunks if c.get("chunk_id") is not None]

    # page + paragraph numbers might be stored in chunk metadata_json (best-effort)
    page_refs: list[int] = []
    paragraph_refs: list[int] = []
    for c in retrieved_chunks:
        meta = c.get("metadata") or c.get("metadata_json") or {}
        # accept both shapes
        pn = meta.get("paragraph_number")
        if pn is not None:
            paragraph_refs.append(int(pn))
        pns = meta.get("paragraph_numbers")
        if isinstance(pns, list):
            paragraph_refs.extend([int(x) for x in pns if x is not None])

        pg = meta.get("page_number")
        if pg is not None:
            page_refs.append(int(pg))

    # official source links if present on retrieved items
    official_links: list[str] = []
    for c in retrieved_chunks:
        link = c.get("official_source_url") or c.get("official_source") or c.get("source_url")
        if link:
            official_links.append(str(link))

    # citations: merge explicit citations argument + inline citations found in answer
    inline_cites = _extract_sources(answer or "")
    source_citations = list(dict.fromkeys(list(citations or []) + inline_cites))

    statute_refs = _extract_statute_refs(answer or "")

    return {
        "answer": answer,
        "source_citations": source_citations,
        "statute_references": statute_refs,
        "paragraph_refs": sorted(set(paragraph_refs)),
        "page_refs": sorted(set(page_refs)),
        "chunk_references": chunk_refs,
        "official_source_links": list(dict.fromkeys(official_links)),
        "hallucination_risk": "low" if source_citations else "medium",
        # UI helpers
        "risk_signals": {
            "citation_count": len(source_citations),
            "statute_count": len(statute_refs),
        },
    }

