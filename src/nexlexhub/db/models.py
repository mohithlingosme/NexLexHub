from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nexlexhub.db.base import Base


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


class Judge(Base, TimestampMixin):
    __tablename__ = "judges"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    court_id: Mapped[Optional[int]] = mapped_column(ForeignKey("courts.id"))
    court: Mapped[Optional["Court"]] = relationship()


class Publisher(Base, TimestampMixin):
    __tablename__ = "publishers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    homepage: Mapped[Optional[str]] = mapped_column(String(500))


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
    legal_issues: Mapped[dict] = mapped_column(JSONB, default=list)
    official_source_url: Mapped[Optional[str]] = mapped_column(String(1000))
    official_source_found: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    decision_date: Mapped[Optional[date]] = mapped_column(Date)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    court: Mapped[Optional["Court"]] = relationship()
    publisher: Mapped[Optional["Publisher"]] = relationship()

    __table_args__ = (UniqueConstraint("normalized_title", "case_number", name="uq_case_title_number"),)


class Statute(Base, TimestampMixin):
    __tablename__ = "statutes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    citation: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000))


class Precedent(Base, TimestampMixin):
    __tablename__ = "precedents"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    cited_case_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cases.id"), nullable=True, index=True)
    cited_text: Mapped[str] = mapped_column(String(500), index=True)
    treatment: Mapped[Optional[str]] = mapped_column(String(100))


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


class LegalEvent(Base, TimestampMixin):
    __tablename__ = "legal_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    headline: Mapped[str] = mapped_column(String(500), index=True)
    publisher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("publishers.id"))
    source_url: Mapped[str] = mapped_column(String(1000), unique=True)
    publish_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), index=True)
    court: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    snippet: Mapped[Optional[str]] = mapped_column(Text)
    entities: Mapped[dict] = mapped_column(JSONB, default=list)
    official_source_found: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    cluster_key: Mapped[Optional[str]] = mapped_column(String(255), index=True)


class JudgmentChunk(Base, TimestampMixin):
    __tablename__ = "judgment_chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, index=True)
    section_tag: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    paragraph_numbers: Mapped[dict] = mapped_column(JSONB, default=list)
    text: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Embedding(Base, TimestampMixin):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey("judgment_chunks.id"), unique=True, index=True)
    provider: Mapped[str] = mapped_column(String(100), index=True)
    vector: Mapped[list[float]] = mapped_column(Vector(16))
    bm25_hint: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
