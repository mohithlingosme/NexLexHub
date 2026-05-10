"""embedding vector dimension migration to 1024

This migration aligns the pgvector column dimension with the production embedding model
(e.g., BAAI/bge-large-en-v1.5 which produces 1024-dim vectors).

Strategy:
- Safely alter the vector column dimension.
- Recreate an ivfflat index with vector_cosine_ops.

Note:
- Existing vectors will be preserved only if pgvector can reinterpret/resize without
  errors. In practice you should re-embed chunks after migrating.
"""

from alembic import op

import sqlalchemy as sa


revision = "20260509_0003"
down_revision = "20260509_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Drop existing ivfflat index (dimension-dependent)
    op.execute("DROP INDEX IF EXISTS ix_embeddings_vector_ivfflat")
    op.execute("DROP INDEX IF EXISTS ix_embeddings_vector_ivfflat_cosine")


    # Alter embeddings.vector to VECTOR(1024)
    # Using raw SQL keeps compatibility across pgvector versions.
    op.execute("ALTER TABLE embeddings ALTER COLUMN vector TYPE vector(1024)")

    # Create ivfflat index for cosine similarity
    # vector_cosine_ops is required for cosine-based ORDER BY.
    op.execute(
        "CREATE INDEX ix_embeddings_vector_ivfflat_cosine "
        "ON embeddings USING ivfflat (vector vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_embeddings_vector_ivfflat_cosine")
    op.execute("ALTER TABLE embeddings ALTER COLUMN vector TYPE vector(16)")
    op.execute("CREATE INDEX ix_embeddings_vector_ivfflat ON embeddings USING ivfflat (vector vector_l2_ops)")

