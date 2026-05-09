from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_index: int
    text: str
    section_tag: str
    paragraph_numbers: list[int]


SECTION_RULES = {
    "facts": re.compile(r"\b(facts|background)\b", re.I),
    "issues": re.compile(r"\b(issue|question for consideration)\b", re.I),
    "analysis": re.compile(r"\b(reason|analysis|held)\b", re.I),
    "order": re.compile(r"\b(order|result|conclusion)\b", re.I),
}


def _detect_section(text: str) -> str:
    for tag, pattern in SECTION_RULES.items():
        if pattern.search(text):
            return tag
    return "body"


def semantic_chunk(text: str, max_chars: int = 1200) -> list[Chunk]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[Chunk] = []
    bucket: list[str] = []
    para_numbers: list[int] = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        if sum(len(p) for p in bucket) + len(paragraph) > max_chars and bucket:
            merged = "\n\n".join(bucket)
            chunks.append(
                Chunk(len(chunks), merged, _detect_section(merged), para_numbers.copy())
            )
            bucket.clear()
            para_numbers.clear()
        bucket.append(paragraph)
        para_numbers.append(idx)
    if bucket:
        merged = "\n\n".join(bucket)
        chunks.append(Chunk(len(chunks), merged, _detect_section(merged), para_numbers.copy()))
    return chunks
