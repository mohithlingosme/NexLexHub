from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class LegalAnalysisResponse(BaseModel):
    query: str
    results: list[dict]
    grounding: dict
    verification: dict
    compliance: dict
    attribution: dict


class CaseOut(BaseModel):
    id: int
    title: str
    citation: str | None = None
    decision_date: date | None = None
    official_source_found: bool
