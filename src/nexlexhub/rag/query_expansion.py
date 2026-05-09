from __future__ import annotations


def expand_query(query: str) -> list[str]:
    tokens = query.split()
    return [query, query.lower(), " ".join(sorted(tokens))]
