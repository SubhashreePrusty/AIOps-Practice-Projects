import time
import streamlit as st
from utils import add_expense_to_api
from datetime import date as dt_date

def show_add_expense():
    st.header("💸 Add New Expense")

    # --- Initialize session state ---
    if "date_input" not in st.session_state:
        st.session_state.date_input = dt_date.today()
    if "category_input" not in st.session_state:
        st.session_state.category_input = "Food"
    if "amount_input" not in st.session_state:
        st.session_state.amount_input = 0.0
    if "note_input" not in st.session_state:
        st.session_state.note_input = ""
    if "reset_form" not in st.session_state:
        st.session_state.reset_form = False
    if "show_toast" not in st.session_state:
        st.session_state.show_toast = False  # 👈 new flag

    # --- Reset logic BEFORE widgets render ---
    if st.session_state.reset_form:
        st.session_state.date_input = dt_date.today()
        st.session_state.category_input = "Food"
        st.session_state.amount_input = 0.0
        st.session_state.note_input = ""
        st.session_state.reset_form = False

    # --- Toast logic ---
    if st.session_state.show_toast:
        st.toast("✅ Expense added successfully!", icon="🎉")
        st.session_state.show_toast = False

    # 🔹 Restrict date range to this month
    today = dt_date.today()
    month_start = today.replace(day=1)

    with st.form("add_expense_form"):
        date = st.date_input(
            "Date",
            min_value=month_start,
            max_value=today,
            key="date_input",
        )

        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Shopping", "Bills", "Other"],
            index=["Food", "Transport", "Shopping", "Bills", "Other"].index(
                st.session_state.category_input
            ),
            key="category_input",
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=0.5,
            # value=st.session_state.amount_input,
            key="amount_input",
        )

        note = st.text_area(
            "Note (optional)",
            value=st.session_state.note_input,
            key="note_input",
        )

        submitted = st.form_submit_button("➕ Add Expense")

        if submitted:
            response = add_expense_to_api(date.strftime("%Y-%m-%d"), category, amount, note)
            if response.get("status") == "success":
                # ✅ Set toast flag and trigger rerun
                st.session_state.show_toast = True
                st.session_state.reset_form = True
                st.rerun()
            else:
                st.error(f"❌ Failed to add expense: {response}")
