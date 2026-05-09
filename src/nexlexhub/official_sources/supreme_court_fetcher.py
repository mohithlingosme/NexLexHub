from __future__ import annotations

import re

from nexlexhub.domain.types import OfficialSourceRecord


def fetch_supreme_court_source(title: str, citation: str | None = None) -> OfficialSourceRecord:
    slug = re.sub(r"[^a-z0-9]+", "-", (citation or title).lower()).strip("-")
    url = f"https://main.sci.gov.in/judgments/{slug}"
    return OfficialSourceRecord("supreme_court", title=title, canonical_url=url, citation=citation)
