from __future__ import annotations

import hashlib
from math import sqrt

from nexlexhub.core.config import get_settings


def generate_embedding(text: str, provider: str | None = None) -> list[float]:
    """Generate an embedding vector.

    Backward compatible behavior:
    - provider == "hash" keeps the legacy deterministic hash embedding.

    Production behavior:
    - provider == "sentence-transformers" uses a local SentenceTransformer.

    Important:
    - The model embedding dimensionality must match settings.embedding_dimension.
      If mismatch, we fall back to the hash strategy for now (so endpoints keep working).
    """

    settings = get_settings()
    dimension = settings.embedding_dimension

    provider = (provider or settings.embedding_provider).lower()

    if provider == "hash":
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = [(digest[i % len(digest)] / 255.0) for i in range(dimension)]
        norm = sqrt(sum(v * v for v in values)) or 1.0
        return [round(v / norm, 6) for v in values]

    # Local sentence-transformers (lazy import to keep startup fast)
    model_name = getattr(settings, "embedding_model", None) or "sentence-transformers/all-MiniLM-L6-v2"

    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        import numpy as np  # type: ignore

        # small in-process cache via function attribute
        cache = getattr(generate_embedding, "_st_cache", {})
        if model_name not in cache:
            cache[model_name] = SentenceTransformer(model_name)
            generate_embedding._st_cache = cache

        model = cache[model_name]
        vec = model.encode([text], normalize_embeddings=True)[0]
        vec = np.asarray(vec, dtype=np.float32)

        if vec.shape[0] != dimension:
            # Dimension mismatch: do not break retrieval; fall back
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            values = [(digest[i % len(digest)] / 255.0) for i in range(dimension)]
            norm = sqrt(sum(v * v for v in values)) or 1.0
            return [round(v / norm, 6) for v in values]

        # pgvector expects Python floats
        return [round(float(x), 6) for x in vec.tolist()]

    except Exception:
        # Hard fallback to keep service stable
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = [(digest[i % len(digest)] / 255.0) for i in range(dimension)]
        norm = sqrt(sum(v * v for v in values)) or 1.0
        return [round(v / norm, 6) for v in values]

