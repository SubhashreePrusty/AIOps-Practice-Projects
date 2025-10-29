import os
import requests
import json
from dotenv import load_dotenv

from utils import get_logger

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv("API_URL")

logger = get_logger(__name__)


def safe_request(method, url, **kwargs):
    """
    Wrapper for making API requests safely with graceful error handling.
    """
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError:
        logger.error("❌ Unable to connect to API Gateway.")
        return {"error": "Could not connect to backend. Check your API Gateway URL or network connection."}
    except requests.exceptions.Timeout:
        logger.error("❌ API request timed out.")
        return {"error": "Request timed out. Please try again later."}
    except requests.exceptions.RequestException as e:
        logger.error("❌ API request failed: %s", e)
        return {"error": f"Unexpected error: {str(e)}"}


# ---- Response handler ----
def _handle_response(resp):
    """Unified response handler."""
    if isinstance(resp, dict) and "error" in resp:
        return resp

    try:
        data = resp.json()
        # Unwrap 'body' if it's a string
        if isinstance(data, dict) and "body" in data and isinstance(data["body"], str):
            try:
                data["body"] = json.loads(data["body"])
                # Merge inner dict if it contains 'items'
                if "items" in data["body"]:
                    data = data["body"]
            except json.JSONDecodeError:
                pass
        return data
    except ValueError:
        logger.error("Invalid JSON in API response.")
        return {"error": "Invalid response from backend."}


# ---- CRUD Operations ----
def add_birthday(name, birthday, email=""):
    payload = {"name": name, "birthday": birthday, "email": email}
    url = f"{API_BASE_URL}/add_birthday"
    resp = safe_request("POST", url, json=payload)
    return _handle_response(resp)


def get_birthdays():
    """Fetch all birthdays safely."""
    url = f"{API_BASE_URL}/get_birthdays"
    resp = safe_request("GET", url)
    data = _handle_response(resp)
    # Unwrap 'body' if it's a string
    if isinstance(data, dict) and "body" in data and isinstance(data["body"], str):
        try:
            data = json.loads(data["body"])
        except json.JSONDecodeError:
            pass

    return data


def delete_birthday(name, birthday):
    """Delete a birthday safely."""
    payload = {"name": name, "birthday": birthday}
    url = f"{API_BASE_URL}/delete_birthday"
    resp = safe_request("DELETE", url, json=payload)
    return _handle_response(resp)
