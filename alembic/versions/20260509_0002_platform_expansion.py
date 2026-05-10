"""expand platform schema"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260509_0002"
down_revision = "20260509_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cases", sa.Column("legal_issues_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.execute("UPDATE cases SET legal_issues_json = legal_issues")
    op.drop_column("cases", "legal_issues")
    op.alter_column("cases", "legal_issues_json", new_column_name="legal_issues", nullable=False)

    op.add_column("cases", sa.Column("metadata_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.execute("UPDATE cases SET metadata_payload = metadata_json")
    op.drop_column("cases", "metadata_json")
    op.alter_column("cases", "metadata_payload", new_column_name="metadata_json", nullable=False)

    op.add_column("statutes", sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False))
    op.add_column("legal_events", sa.Column("event_hash", sa.String(length=128), nullable=True))
    op.create_index("ix_legal_events_event_hash", "legal_events", ["event_hash"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.create_index("ix_users_is_active", "users", ["is_active"], unique=False)

    op.create_table(
        "judgments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=False),
        sa.Column("document_type", sa.String(length=100), nullable=False),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("local_path", sa.String(length=1000), nullable=True),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
        sa.Column("extracted_text", sa.Text(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_judgments_case_id", "judgments", ["case_id"], unique=False)
    op.create_index("ix_judgments_document_type", "judgments", ["document_type"], unique=False)
    op.create_index("ix_judgments_checksum", "judgments", ["checksum"], unique=True)

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("query", sa.String(length=500), nullable=False),
        sa.Column("delivery_channel", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_alerts_user_id", "alerts", ["user_id"], unique=False)
    op.create_index("ix_alerts_query", "alerts", ["query"], unique=False)
    op.create_index("ix_alerts_is_active", "alerts", ["is_active"], unique=False)

    op.create_table(
        "ai_conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("sources_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_conversations_user_id", "ai_conversations", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_table("ai_conversations")
    op.drop_table("alerts")
    op.drop_table("judgments")
    op.drop_table("users")
    op.drop_index("ix_legal_events_event_hash", table_name="legal_events")
    op.drop_column("legal_events", "event_hash")
    op.drop_column("statutes", "metadata_json")
