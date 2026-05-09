from __future__ import annotations

from nexlexhub.compliance.copyright_checker import copyright_risk_score
from nexlexhub.compliance.source_similarity import similarity_score


def evaluate(text: str, snippet: str) -> dict[str, float]:
    return {
        "copyright_risk": copyright_risk_score(text, snippet),
        "publisher_overlap": similarity_score(text, snippet),
    }
