from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DiscoveryRecord:
    headline: str
    publisher: str
    source_url: str
    publish_date: str
    court: str
    snippet: str
    entities: list[str] = field(default_factory=list)
    official_source_found: bool = False


@dataclass
class OfficialSourceRecord:
    source_type: str
    title: str
    canonical_url: str
    citation: str | None = None
    case_number: str | None = None
    retrieved_at: datetime = field(default_factory=datetime.utcnow)
    local_path: str | None = None
