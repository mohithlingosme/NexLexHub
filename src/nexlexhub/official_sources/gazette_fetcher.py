from __future__ import annotations

import re

from nexlexhub.domain.types import OfficialSourceRecord


def fetch_gazette_source(title: str) -> OfficialSourceRecord:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return OfficialSourceRecord(
        "gazette",
        title=title,
        canonical_url=f"https://egazette.nic.in/search/{slug}",
    )
