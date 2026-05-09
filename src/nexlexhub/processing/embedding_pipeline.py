from __future__ import annotations

import hashlib
from math import sqrt

from nexlexhub.core.config import get_settings


def generate_embedding(text: str, provider: str | None = None) -> list[float]:
    settings = get_settings()
    dimension = settings.embedding_dimension
    provider = provider or settings.embedding_provider
    if provider != "hash":
        provider = "hash"
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [(digest[i % len(digest)] / 255.0) for i in range(dimension)]
    norm = sqrt(sum(v * v for v in values)) or 1.0
    return [round(v / norm, 6) for v in values]
