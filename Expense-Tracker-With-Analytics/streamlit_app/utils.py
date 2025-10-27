# Functions to call API Gateway endpoints


# utils.py
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_URL")

def add_expense_to_api(date, category, amount, note):
    """Send new expense data to backend Lambda"""
    payload = {
        "date": date,
        "category": category,
        "amount": float(amount),
        "note": note
    }
    response = requests.post(f"{API_BASE_URL}/expenses", json=payload)
    return response.json()

def get_all_expenses():
    """Fetch all expenses from backend Lambda"""
    response = requests.get(f"{API_BASE_URL}/expenses")
    data = response.json()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_category_summary():
    """Fetch category-wise summary (optional endpoint)"""
    response = requests.get(f"{API_BASE_URL}/summary")
    data = response.json()
    return pd.DataFrame(data)
