# delete_expense.py
import streamlit as st
from utils import delete_expense_from_api

def handle_delete_expense(row):
    """Handle delete operation for a single expense"""
    if "month_category" in row and "date_id" in row:
        resp = delete_expense_from_api(row["month_category"], row["date_id"])
        if resp.get("status") == "success":
            st.success("🗑️ Expense deleted successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to delete expense.")
    else:
        st.error("⚠️ Missing keys for deletion — cannot delete this record.")
