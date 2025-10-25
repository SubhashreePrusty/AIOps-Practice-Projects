# Helper functions (e.g., date formatting)
import datetime
import logging

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

