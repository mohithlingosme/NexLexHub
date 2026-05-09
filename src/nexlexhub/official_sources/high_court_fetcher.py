from __future__ import annotations

import re

from nexlexhub.domain.types import OfficialSourceRecord


def fetch_high_court_source(title: str, court: str, citation: str | None = None) -> OfficialSourceRecord:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    court_slug = re.sub(r"[^a-z0-9]+", "-", court.lower()).strip("-")
    url = f"https://{court_slug}.gov.in/judgments/{slug}"
    return OfficialSourceRecord("high_court", title=title, canonical_url=url, citation=citation)
