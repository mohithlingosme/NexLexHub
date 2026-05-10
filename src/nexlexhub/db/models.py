from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexlexhub.db.base import Base
from nexlexhub.db.types import json_type, vector_type


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Court(Base, TimestampMixin):
    __tablename__ = "courts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    level: Mapped[str] = mapped_column(String(50), index=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cases: Mapped[list["Case"]] = relationship(back_populates="court")
    judges: Mapped[list["Judge"]] = relationship(back_populates="court")


class Judge(Base, TimestampMixin):
    __tablename__ = "judges"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    court_id: Mapped[Optional[int]] = mapped_column(ForeignKey("courts.id"))
    court: Mapped[Optional["Court"]] = relationship(back_populates="judges")


class Publisher(Base, TimestampMixin):
    __tablename__ = "publishers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    homepage: Mapped[Optional[str]] = mapped_column(String(500))
    cases: Mapped[list["Case"]] = relationship(back_populates="publisher")
    legal_events: Mapped[list["LegalEvent"]] = relationship(back_populates="publisher")


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), index=True, default="reader")
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    alerts: Mapped[list["Alert"]] = relationship(back_populates="user")
    conversations: Mapped[list["AIConversation"]] = relationship(back_populates="user")


class Case(Base, TimestampMixin):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    normalized_title: Mapped[str] = mapped_column(String(500), index=True)
    case_number: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    citation: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    court_id: Mapped[Optional[int]] = mapped_column(ForeignKey("courts.id"))
    publisher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("publishers.id"))
    bench: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    ratio_decidendi: Mapped[Optional[str]] = mapped_column(Text)
    obiter_dicta: Mapped[Optional[str]] = mapped_column(Text)
    procedural_posture: Mapped[Optional[str]] = mapped_column(Text)
    legal_issues: Mapped[list[str]] = mapped_column(json_type(), default=list)
    official_source_url: Mapped[Optional[str]] = mapped_column(String(1000))
    official_source_found: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    decision_date: Mapped[Optional[date]] = mapped_column(Date)
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    court: Mapped[Optional["Court"]] = relationship(back_populates="cases")
    publisher: Mapped[Optional["Publisher"]] = relationship(back_populates="cases")
    judgments: Mapped[list["Judgment"]] = relationship(back_populates="case")
    chunks: Mapped[list["JudgmentChunk"]] = relationship(back_populates="case")
    citations: Mapped[list["Citation"]] = relationship(back_populates="case")
    outgoing_precedents: Mapped[list["Precedent"]] = relationship(
        foreign_keys="Precedent.source_case_id", back_populates="source_case"
    )
    incoming_precedents: Mapped[list["Precedent"]] = relationship(
        foreign_keys="Precedent.cited_case_id", back_populates="cited_case"
    )

    __table_args__ = (UniqueConstraint("normalized_title", "case_number", name="uq_case_title_number"),)


class Statute(Base, TimestampMixin):
    __tablename__ = "statutes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    citation: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000))
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)


class Judgment(Base, TimestampMixin):
    __tablename__ = "judgments"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    document_type: Mapped[str] = mapped_column(String(100), default="judgment", index=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000))
    local_path: Mapped[Optional[str]] = mapped_column(String(1000))
    checksum: Mapped[Optional[str]] = mapped_column(String(128), unique=True, index=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    extracted_text: Mapped[Optional[str]] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    case: Mapped["Case"] = relationship(back_populates="judgments")


class Precedent(Base, TimestampMixin):
    __tablename__ = "precedents"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    cited_case_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cases.id"), nullable=True, index=True)
    cited_text: Mapped[str] = mapped_column(String(500), index=True)
    treatment: Mapped[Optional[str]] = mapped_column(String(100))
    source_case: Mapped["Case"] = relationship(foreign_keys=[source_case_id], back_populates="outgoing_precedents")
    cited_case: Mapped[Optional["Case"]] = relationship(
        foreign_keys=[cited_case_id], back_populates="incoming_precedents"
    )


class Citation(Base, TimestampMixin):
    __tablename__ = "citations"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cases.id"), index=True)
    chunk_id: Mapped[Optional[int]] = mapped_column(ForeignKey("judgment_chunks.id"), index=True)
    raw_text: Mapped[str] = mapped_column(String(500), index=True)
    normalized_text: Mapped[str] = mapped_column(String(500), index=True)
    citation_type: Mapped[str] = mapped_column(String(100), index=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000))
    case: Mapped[Optional["Case"]] = relationship(back_populates="citations")
    chunk: Mapped[Optional["JudgmentChunk"]] = relationship(back_populates="citations")


class LegalEvent(Base, TimestampMixin):
    __tablename__ = "legal_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    headline: Mapped[str] = mapped_column(String(500), index=True)
    publisher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("publishers.id"))
    source_url: Mapped[str] = mapped_column(String(1000), unique=True)
    publish_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), index=True)
    court: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    snippet: Mapped[Optional[str]] = mapped_column(Text)
    entities: Mapped[list[str]] = mapped_column(json_type(), default=list)
    official_source_found: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    cluster_key: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    event_hash: Mapped[Optional[str]] = mapped_column(String(128), unique=True, index=True)
    publisher: Mapped[Optional["Publisher"]] = relationship(back_populates="legal_events")


class JudgmentChunk(Base, TimestampMixin):
    __tablename__ = "judgment_chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, index=True)
    section_tag: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    paragraph_numbers: Mapped[list[int]] = mapped_column(json_type(), default=list)
    text: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    case: Mapped["Case"] = relationship(back_populates="chunks")
    citations: Mapped[list["Citation"]] = relationship(back_populates="chunk")
    embedding: Mapped[Optional["Embedding"]] = relationship(back_populates="chunk")


class Embedding(Base, TimestampMixin):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey("judgment_chunks.id"), unique=True, index=True)
    provider: Mapped[str] = mapped_column(String(100), index=True)
    vector: Mapped[list[float]] = mapped_column(vector_type(1024))
    bm25_hint: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    chunk: Mapped["JudgmentChunk"] = relationship(back_populates="embedding")


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    query: Mapped[str] = mapped_column(String(500), index=True)
    delivery_channel: Mapped[str] = mapped_column(String(50), default="in_app")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    user: Mapped["User"] = relationship(back_populates="alerts")


class AIConversation(Base, TimestampMixin):
    __tablename__ = "ai_conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), default="Untitled conversation")
    query: Mapped[str] = mapped_column(Text)
    answer: Mapped[Optional[str]] = mapped_column(Text)
    sources_json: Mapped[list[dict]] = mapped_column(json_type(), default=list)
    metadata_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    user: Mapped[Optional["User"]] = relationship(back_populates="conversations")
