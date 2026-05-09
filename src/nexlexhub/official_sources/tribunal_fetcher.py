from __future__ import annotations

import re

from nexlexhub.domain.types import OfficialSourceRecord


def fetch_tribunal_source(title: str, citation: str | None = None) -> OfficialSourceRecord:
    slug = re.sub(r"[^a-z0-9]+", "-", (citation or title).lower()).strip("-")
    return OfficialSourceRecord(
        "tribunal",
        title=title,
        canonical_url=f"https://tribunals.gov.in/judgments/{slug}",
        citation=citation,
    )
