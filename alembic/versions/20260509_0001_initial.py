"""initial schema"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql


revision = "20260509_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "courts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("jurisdiction", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_courts_name", "courts", ["name"], unique=True)
    op.create_index("ix_courts_slug", "courts", ["slug"], unique=True)
    op.create_index("ix_courts_level", "courts", ["level"], unique=False)

    op.create_table(
        "judges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("court_id", sa.Integer(), sa.ForeignKey("courts.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_judges_name", "judges", ["name"], unique=True)

    op.create_table(
        "publishers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("homepage", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_publishers_name", "publishers", ["name"], unique=True)

    op.create_table(
        "cases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("normalized_title", sa.String(length=500), nullable=False),
        sa.Column("case_number", sa.String(length=255), nullable=True),
        sa.Column("citation", sa.String(length=255), nullable=True),
        sa.Column("court_id", sa.Integer(), sa.ForeignKey("courts.id")),
        sa.Column("publisher_id", sa.Integer(), sa.ForeignKey("publishers.id")),
        sa.Column("bench", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("ratio_decidendi", sa.Text(), nullable=True),
        sa.Column("obiter_dicta", sa.Text(), nullable=True),
        sa.Column("procedural_posture", sa.Text(), nullable=True),
        sa.Column("legal_issues", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("official_source_url", sa.String(length=1000), nullable=True),
        sa.Column("official_source_found", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("decision_date", sa.Date(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("normalized_title", "case_number", name="uq_case_title_number"),
    )
    for idx in ["title", "normalized_title", "case_number", "citation", "official_source_found"]:
        op.create_index(f"ix_cases_{idx}", "cases", [idx], unique=False)

    op.create_table(
        "statutes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("citation", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_statutes_name", "statutes", ["name"], unique=True)
    op.create_index("ix_statutes_citation", "statutes", ["citation"], unique=False)

    op.create_table(
        "precedents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=False),
        sa.Column("cited_case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=True),
        sa.Column("cited_text", sa.String(length=500), nullable=False),
        sa.Column("treatment", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    for idx in ["source_case_id", "cited_case_id"]:
        op.create_index(f"ix_precedents_{idx}", "precedents", [idx], unique=False)

    op.create_table(
        "legal_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("headline", sa.String(length=500), nullable=False),
        sa.Column("publisher_id", sa.Integer(), sa.ForeignKey("publishers.id")),
        sa.Column("source_url", sa.String(length=1000), nullable=False),
        sa.Column("publish_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("court", sa.String(length=255), nullable=True),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("entities", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("official_source_found", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("cluster_key", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_url"),
    )
    for idx in ["headline", "publish_date", "court", "official_source_found", "cluster_key"]:
        op.create_index(f"ix_legal_events_{idx}", "legal_events", [idx], unique=False)

    op.create_table(
        "judgment_chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("section_tag", sa.String(length=100), nullable=True),
        sa.Column("paragraph_numbers", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    for idx in ["case_id", "chunk_index", "section_tag"]:
        op.create_index(f"ix_judgment_chunks_{idx}", "judgment_chunks", [idx], unique=False)

    op.create_table(
        "citations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=True),
        sa.Column("chunk_id", sa.Integer(), sa.ForeignKey("judgment_chunks.id"), nullable=True),
        sa.Column("raw_text", sa.String(length=500), nullable=False),
        sa.Column("normalized_text", sa.String(length=500), nullable=False),
        sa.Column("citation_type", sa.String(length=100), nullable=False),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    for idx in ["case_id", "chunk_id", "raw_text", "normalized_text", "citation_type", "verified"]:
        op.create_index(f"ix_citations_{idx}", "citations", [idx], unique=False)

    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chunk_id", sa.Integer(), sa.ForeignKey("judgment_chunks.id"), nullable=False, unique=True),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column("vector", Vector(dim=16), nullable=False),
        sa.Column("bm25_hint", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_embeddings_chunk_id", "embeddings", ["chunk_id"], unique=True)
    op.create_index("ix_embeddings_provider", "embeddings", ["provider"], unique=False)
    op.execute("CREATE INDEX IF NOT EXISTS ix_embeddings_vector_ivfflat ON embeddings USING ivfflat (vector vector_l2_ops)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_embeddings_vector_ivfflat")
    for table in ["embeddings", "citations", "judgment_chunks", "legal_events", "precedents", "statutes", "cases", "publishers", "judges", "courts"]:
        op.drop_table(table)
