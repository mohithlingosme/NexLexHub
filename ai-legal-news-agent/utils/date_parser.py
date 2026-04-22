import logging
import re
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
_MONTH_MAP = {m.lower(): i + 1 for i, m in enumerate(_MONTHS)}
_HUMAN_DATE_RE = re.compile(
    r"(?P<month>[A-Za-z]+)\s+(?P<day>\d{1,2}),\s+(?P<year>\d{4})(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{2}))?"
)


def parse_date(date_str: str) -> datetime:
    """Parse ISO or common human formats. Returns datetime.min on failure."""
    if not date_str or not isinstance(date_str, str):
        return datetime.min

    s = date_str.strip()
    if not s:
        return datetime.min

    # ISO 8601 (common from JSON-LD): 2026-04-22T10:11:12Z
    try:
        s2 = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s2)
    except ValueError:
        pass

    # "April 22, 2026" or "April 22, 2026 10:15"
    m = _HUMAN_DATE_RE.search(s)
    if m:
        month = _MONTH_MAP.get(m.group("month").lower())
        if month:
            day = int(m.group("day"))
            year = int(m.group("year"))
            hour = int(m.group("hour") or 0)
            minute = int(m.group("minute") or 0)
            return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

    # "22 April 2026"
    try:
        return datetime.strptime(s, "%d %B %Y")
    except ValueError:
        pass

    logger.warning("Unparseable date: %r", s)
    return datetime.min


def format_date(dt: datetime) -> str:
    if dt == datetime.min:
        return ""
    return dt.isoformat()

