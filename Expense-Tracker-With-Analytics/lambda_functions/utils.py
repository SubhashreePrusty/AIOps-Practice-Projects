# Common backend utilities
import json
from datetime import datetime, timezone

def response(status_code, body):
    """Standardized Lambda API response"""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def get_current_timestamp():
    """Get current UTC timestamp"""
    return datetime.now(timezone.utc).isoformat()
