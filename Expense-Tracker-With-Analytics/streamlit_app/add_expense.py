
# add_expense.py
import streamlit as st
from utils import add_expense_to_api

def show_add_expense():
    st.header("💸 Add New Expense")

    with st.form("add_expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
        note = st.text_area("Note (optional)")
        
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            response = add_expense_to_api(date.strftime("%Y-%m-%d"), category, amount, note)
            if response.get("status") == "success":
                st.success("✅ Expense added successfully!")
            else:
                st.error(f"❌ Failed to add expense: {response}")