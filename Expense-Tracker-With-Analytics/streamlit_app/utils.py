# utils.py
import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")

def add_expense_to_api(date, category, amount, note):
    """Send new expense data to backend Lambda"""
    payload = {
        "date": date,
        "category": category,
        "amount": float(amount),
        "note": note
    }
    try:
        response = requests.post(f"{API_URL}/expenses", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to connect to API: {e}")
        return {"status": "error"}

def get_all_expenses():
    """Fetch all expenses from backend Lambda"""
    try:
        response = requests.get(f"{API_URL}/expenses")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch expenses: {e}")
        return pd.DataFrame()

def get_category_summary():
    """Fetch category-wise summary (optional endpoint)"""
    try:
        response = requests.get(f"{API_URL}/summary")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch summary: {e}")
        return pd.DataFrame()
        