# Helper functions (e.g., date formatting)
import datetime
import logging
from datetime import date, datetime
from typing import List, Dict

def _parse_iso(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()

def days_until_next(bday: date, today: date) -> int:
    this_year_occurrence = date(today.year, bday.month, bday.day)
    if this_year_occurrence >= today:
        return (this_year_occurrence - today).days
    else:
        next_occurrence = date(today.year + 1, bday.month, bday.day)
        return (next_occurrence - today).days

def next_birthdays(records: List[Dict], count: int = 3, today: date | None = None) -> List[Dict]:
    if today is None:
        today = date.today()

    enriched = []
    for r in records:
        try:
            birth = _parse_iso(r["date"])
        except Exception:
            continue

        try:
            candidate = date(today.year, birth.month, birth.day)
        except ValueError:
            candidate = date(today.year, 3, 1)

        if candidate < today:
            try:
                candidate = date(today.year + 1, birth.month, birth.day)
            except ValueError:
                candidate = date(today.year + 1, 3, 1)

        days_left = (candidate - today).days
        age_on_next = candidate.year - birth.year

        enriched.append({
            **r,
            "next_date": candidate.isoformat(),
            "days_left": days_left,
            "age_on_next": age_on_next
        })

    # sort all by upcoming date
    enriched.sort(key=lambda x: x["days_left"])

    # collect birthdays within next `count` distinct dates
    grouped = []
    seen_dates = set()
    for rec in enriched:
        nd = rec["next_date"]
        if len(seen_dates) < count or nd in seen_dates:
            grouped.append(rec)
            seen_dates.add(nd)
        else:
            break

    return grouped

def format_birthday(date_obj):
    """
    Takes a datetime.date object and returns a string in ISO format (YYYY-MM-DD).
    Example: 2025-10-25
    """
    if isinstance(date_obj, date):
        return date_obj.strftime("%Y-%m-%d")
    raise ValueError("Input must be a datetime.date object")

def is_future_date(date_obj):
    """Check if the given date is in the future."""
    today = date.today()
    return date_obj > today


def get_logger(name: str):
    """
    Returns a configured logger with a consistent format across the app.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent duplicate handlers if re-imported
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

