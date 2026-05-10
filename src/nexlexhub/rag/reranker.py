from __future__ import annotations

import re
from datetime import datetime
from typing import Any





_COURT_PRIORITY = {

    "Supreme Court": 1.0,
    "Supreme Court of India": 1.0,
    "High Court": 0.7,
}


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _tokenize(s: str) -> set[str]:
    s = s.lower()
    return set(re.findall(r"[a-z0-9]+(?:\/[a-z0-9]+)*", s))


def rerank(items: list[dict], *, query: str | None = None) -> list[dict]:
    """Factor-based reranker.

    Backward compatible behavior:
    - If `query` is not provided, preserve legacy meaning of `score`.
    - If `query` is provided, recompute a richer score.
    """

    # Backward compatibility for tests and older callers.
    if not query:
        return sorted(items, key=lambda item: (item.get("score", 0.0), item.get("verified", False)), reverse=True)

    q_tokens = _tokenize(query or "")
    q_text = (query or "").lower().strip()


    now = datetime.utcnow()

    def court_priority(court: str | None) -> float:
        if not court:
            return 0.5
        for k, v in _COURT_PRIORITY.items():
            if k.lower() in court.lower():
                return v
        # if it looks like a high court
        if "high court" in court.lower():
            return 0.7
        return 0.5

    reranked: list[dict] = []

    for item in items:
        # semantic score (already computed upstream)
        base_sem = _safe_float(item.get("score"), 0.0)

        # metadata fields (may be absent in old chunks)
        chunk_text = item.get("text", "") or ""
        case_citation = item.get("citation") or ""
        court = item.get("court")
        decision_date = item.get("decision_date")
        is_verified = bool(item.get("verified", False))

        # exact phrase matches
        exact_phrase_hits = 0
        if q_text:
            # naive phrase: full query
            if q_text and q_text in chunk_text.lower():
                exact_phrase_hits += 1
            # also check common legal chunk prefixes
            for phrase in ["section", "article", "court", "held", "ratio", "decision"]:
                if phrase in q_text and phrase in chunk_text.lower():
                    exact_phrase_hits += 0.5

        # overlap signals
        if q_tokens:
            chunk_tokens = _tokenize(chunk_text)
            legal_term_overlap = len(q_tokens & chunk_tokens) / (len(q_tokens) or 1)
        else:
            legal_term_overlap = 0.0

        # citation / statute overlap
        citation_refs = item.get("citation_references") or []
        statute_refs = item.get("statute_references") or []

        citation_overlap = 0.0
        if q_text:
            q_lower = q_text
            for c in citation_refs:
                if c.lower() in q_lower:
                    citation_overlap += 1.0

        statute_overlap = 0.0
        if q_text:
            q_lower = q_text
            for s in statute_refs:
                if s.lower() in q_lower:
                    statute_overlap += 1.0

        # recency
        recency = 0.0
        if isinstance(decision_date, str) and decision_date:
            try:
                dt = datetime.fromisoformat(decision_date)
            except Exception:
                dt = None
            if dt:
                days = max(0.0, (now - dt).total_seconds() / 86400.0)
                recency = 1.0 / (1.0 + days / 365.0)
        elif decision_date is not None:
            recency = 0.2

        # court priority
        cp = court_priority(court or ("Supreme Court" if "SCC" in case_citation else None))

        # weighted score
        score = 0.0
        score += base_sem * 0.55
        score += (citation_overlap * 0.35)  # strong
        score += (statute_overlap * 0.25)  # strong
        score += (legal_term_overlap * 0.25)
        score += (exact_phrase_hits * 0.2)
        score += (cp * 0.1)
        score += (recency * 0.1)
        score += (0.05 if is_verified else 0.0)

        item = dict(item)
        item["score"] = round(score, 4)
        item["rerank_factors"] = {
            "base_sem": round(base_sem, 4),
            "citation_overlap": citation_overlap,
            "statute_overlap": statute_overlap,

            "legal_term_overlap": round(legal_term_overlap, 4),
            "exact_phrase_hits": exact_phrase_hits,
            "court_priority": cp,
            "recency": round(recency, 4),
            "verified_boost": 0.05 if is_verified else 0.0,
        }
        reranked.append(item)

    reranked.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    return reranked

