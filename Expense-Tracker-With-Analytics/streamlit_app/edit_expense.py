import streamlit as st
import pandas as pd
from utils import update_expense_in_api

def edit_expense_form(row, i):
    """Render an editable Streamlit form for a single expense"""
    with st.expander(f"✏️ Edit {row['category']} on {row['date']}", expanded=True):
        with st.form(f"edit_form_{i}"):

            st.write("Update details below:")

            categories = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Other"]
            new_date = st.date_input("Date", pd.to_datetime(row["date"]))
            new_category = st.selectbox(
                "Category",
                categories,
                index=categories.index(row["category"]) if row["category"] in categories else len(categories) - 1
            )
            new_amount = st.number_input("Amount", min_value=0.0, value=float(row["amount"]), step=10.0)
            new_note = st.text_area("Note", value=row.get("note", ""))

            # --- Save and Cancel Buttons ---
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("💾 Save Changes")
            with col2:
                cancel = st.form_submit_button("❌ Cancel")

            # --- Handle Save ---
            if submitted:
                resp = update_expense_in_api(
                    row.get("month_category"),
                    row.get("date_id"),
                    new_category,
                    new_amount,
                    new_note
                )

                backend_resp = resp.get("response", {})
                status = backend_resp.get("status") or resp.get("status")

                if status == "success":
                    st.success("✅ Expense updated successfully!")
                    st.session_state.edit_index = None
                    st.rerun()
                else:
                    st.error("❌ Failed to update expense.")
                    st.write("Full API response:", resp)

            # --- Handle Cancel ---
            if cancel:
                st.session_state.edit_index = None
                st.rerun()
