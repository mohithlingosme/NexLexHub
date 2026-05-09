from __future__ import annotations

import re
from typing import Any

from nexlexhub.processing.citation_extractor import extract_citations


CASE_NUMBER_PATTERN = re.compile(r"(?:C\.A\.|W\.P\.|SLP|Cr\.A\.|CIVIL APPEAL)\s*No\.?\s*[\w/-]+", re.I)
COURT_PATTERN = re.compile(r"\b(Supreme Court|[A-Z][a-z]+ High Court|Tribunal)\b")
JUDGE_PATTERN = re.compile(r"Justice\s+[A-Z][A-Za-z.\s]+")


def extract_metadata(text: str, title: str = "") -> dict[str, Any]:
    citations = extract_citations(text)
    issues = []
    for token in ["insolvency", "arbitration", "constitutional", "tax", "criminal", "civil"]:
        if token in text.lower():
            issues.append(token)
    court_match = COURT_PATTERN.search(text) or COURT_PATTERN.search(title)
    case_match = CASE_NUMBER_PATTERN.search(text)
    return {
        "title": title,
        "court": court_match.group(0) if court_match else None,
        "bench": ", ".join(sorted(set(m.group(0).strip() for m in JUDGE_PATTERN.finditer(text)))) or None,
        "case_number": case_match.group(0) if case_match else None,
        "statutes": [c["raw_text"] for c in citations if c["citation_type"] == "statute"],
        "precedents": [c["raw_text"] for c in citations if c["citation_type"] != "statute"],
        "legal_issues": issues,
        "ratio_decidendi": text[:400],
        "obiter_dicta": text[400:700] if len(text) > 500 else "",
        "procedural_posture": "discovered_from_official_source",
    }
