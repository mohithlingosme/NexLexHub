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


class StatuteOut(BaseModel):
    id: int
    name: str
    citation: str | None = None
    source_url: str | None = None


class AlertOut(BaseModel):
    id: int
    name: str
    query: str
    delivery_channel: str
    is_active: bool


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class ChatRequest(BaseModel):
    query: str
    title: str | None = None


class ConversationOut(BaseModel):
    id: int
    title: str
    query: str
    answer: str | None = None
    sources_json: list[dict] = []
