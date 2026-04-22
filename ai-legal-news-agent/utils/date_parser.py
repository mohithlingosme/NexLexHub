from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_date(date_str: str) -> datetime:
    \"\"\"Parse ISO date from scraper, fallback to min date.\"\"\"
    try:
        # Remove Z and normalize
        date_str = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        logger.warning(f"Invalid date: {date_str}")
        return datetime.min

def format_date(dt: datetime) -> str:
    \"\"\"Format datetime to ISO string.\"\"\"
    if dt == datetime.min:
        return ''
    return dt.isoformat()

