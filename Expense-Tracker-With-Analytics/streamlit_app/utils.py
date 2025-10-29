# utils.py
import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

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

        # Convert to DataFrame
        df = pd.DataFrame(data) if data else pd.DataFrame()

        # Keep only the required columns (if they exist)
        expected_cols = ["category", "amount", "date", "note"]
        df = df[[col for col in expected_cols if col in df.columns]]

        return df
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch expenses: {e}")
        return pd.DataFrame()

def get_category_summary():
    """Fetch category-wise summary for the current month up to today"""
    try:
        # Automatically determine current month (YYYY-MM)
        current_month = datetime.now().strftime("%Y-%m")

        # Hit the summary endpoint with month param
        response = requests.get(f"{API_URL}/summary", params={"month": current_month})
        response.raise_for_status()
        data = response.json()

        # Convert to DataFrame
        if data and isinstance(data, list):
            df = pd.DataFrame(data)
            if "category" in df.columns and "total" in df.columns:
                return df
            else:
                st.warning("⚠️ Backend data missing 'category' or 'total' fields.")
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch summary: {e}")
        return pd.DataFrame()

# 🟢 Update Expense
def update_expense_in_api(month_category, date_id, category, amount, note):
    """Update an existing expense via API"""
    payload = {
        "month_category": month_category,
        "date_id": date_id,
        "category": category,
        "amount": float(amount),
        "note": note
    }
    try:
        response = requests.put(f"{API_URL}/expenses", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to update expense: {e}")
        return {"status": "error"}


# 🟢 Delete Expense
def delete_expense_from_api(month_category, date_id):
    """Delete an expense via API (send as query params)"""
    params = {"month_category": month_category, "date_id": date_id}
    try:
        response = requests.delete(f"{API_URL}/expenses", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to delete expense: {e}")
        return {"status": "error"}


        