from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeEngine


def json_type() -> TypeEngine:
    return JSON().with_variant(JSONB(astext_type=Text()), "postgresql")


def vector_type(dimensions: int) -> TypeEngine:
    # pgvector column must be sized; SQLite fallback remains JSON.
    return Vector(dimensions).with_variant(JSON(), "sqlite")
