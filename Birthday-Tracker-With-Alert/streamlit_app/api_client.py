# streamlit_app/api_client.py
import os
import requests
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
        # This happens if safe_request returned an error dict
        return resp

    try:
        return resp.json()
    except ValueError:
        logger.error("Invalid JSON in API response.")
        return {"error": "Invalid response from backend."}

# ---- CRUD Operations ----
def add_birthday(name, birthday):
    payload = {"name": name, "birthday": birthday}
    url = f"{API_BASE_URL}/add_birthday"
    logger.info("📤 Adding birthday: %s", payload)
    resp = safe_request("POST", url, json=payload)
    return _handle_response(resp)

def get_birthdays():
    logger.info("📥 Fetching all birthdays")
    url = f"{API_BASE_URL}/get_birthdays"
    resp = safe_request("GET", url)
    return _handle_response(resp)

def edit_birthday(name, new_date):
    payload = {"name": name, "new_birthday": new_date}
    logger.info("✏️ Editing birthday: %s", payload)
    url = f"{API_BASE_URL}/edit_birthday"
    resp = safe_request("PUT", url, json=payload)
    return _handle_response(resp)

def delete_birthday(name):
    payload = {"name": name}
    logger.info("🗑️ Deleting birthday for %s", name)
    url = f"{API_BASE_URL}/delete_birthday"
    resp = safe_request("DELETE", url, json=payload)
    return _handle_response(resp)
