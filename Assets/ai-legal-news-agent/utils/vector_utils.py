from __future__ import annotations

import hashlib
import math
from typing import List, Sequence

from utils.file_utils import normalize_text


def l2_normalize(vec: Sequence[float]) -> List[float]:
    out = [float(x) for x in vec]
    s = 0.0
    for x in out:
        s += x * x
    n = math.sqrt(s)
    if not n:
        return out
    return [x / n for x in out]


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    den = math.sqrt(na) * math.sqrt(nb)
    return dot / den if den else 0.0


def hash_embed(text: str, *, dim: int = 256) -> List[float]:
    """
    Dependency-free deterministic embedding.
    Not semantic, but stable and sufficient for local smoke-testing.
    """
    counts = [0.0] * dim
    for tok in normalize_text(text).lower().split():
        h = int(hashlib.sha256(tok.encode("utf-8")).hexdigest(), 16)
        counts[h % dim] += 1.0
    return l2_normalize(counts)
