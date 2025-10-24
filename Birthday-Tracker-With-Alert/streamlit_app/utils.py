# Helper functions (e.g., date formatting)
# streamlit_app/utils.py
import datetime

def format_birthday(date_obj):
    """
    Takes a datetime.date object and returns a string in ISO format (YYYY-MM-DD).
    Example: 2025-10-25
    """
    if isinstance(date_obj, datetime.date):
        return date_obj.strftime("%Y-%m-%d")
    raise ValueError("Input must be a datetime.date object")

def is_future_date(date_obj):
    """Check if the given date is in the future."""
    today = datetime.date.today()
    return date_obj > today
