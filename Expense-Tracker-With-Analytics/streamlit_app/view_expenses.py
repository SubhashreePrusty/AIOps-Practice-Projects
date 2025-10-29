
# view_expenses.py
import streamlit as st
import requests
import pandas as pd
from utils import (
    get_all_expenses,
    get_category_summary,
    update_expense_in_api,
    delete_expense_from_api
)


def show_view_expenses():
    st.header("📊 View & Manage Expenses")

    df_full = get_all_expenses()

    if df_full.empty:
        st.warning("No expenses found yet. Add some!")
        return

    # ✅ Keep full data for backend keys, but only show required columns to user
    expected_cols = ["date", "category", "amount", "note", "month_category", "date_id"]
    df_full = df_full[[c for c in expected_cols if c in df_full.columns]]

    display_cols = ["date", "category", "amount", "note"]
    st.write("### 💸 Expense List")

    # ✅ Table headers
    header_cols = st.columns([2, 2, 2, 3, 1, 1])
    headers = ["Date", "Category", "Amount", "Note", "Edit", "Delete"]
    for col, name in zip(header_cols, headers):
        col.markdown(f"**{name}**")

    # ✅ Loop through each expense
    for i, row in df_full.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])

        col1.write(row.get("date", "-"))
        col2.write(row.get("category", "-"))
        col3.write(f"₹{row.get('amount', 0):.2f}")
        col4.write(row.get("note", "-"))

        edit_btn = col5.button("✏️", key=f"edit_{i}")
        del_btn = col6.button("🗑️", key=f"del_{i}")

        # --- Handle Edit action ---
        if edit_btn:
            with st.form(f"edit_form_{i}", clear_on_submit=True):
                st.subheader("✏️ Edit Expense")

                new_date = st.date_input("Date", pd.to_datetime(row["date"]))
                new_category = st.text_input("Category", value=row["category"])
                new_amount = st.number_input("Amount", value=float(row["amount"]))
                new_note = st.text_area("Note", value=row["note"] or "")

                submitted = st.form_submit_button("💾 Save Changes")

                if submitted:
                    resp = update_expense_in_api(
                        row.get("month_category"), 
                        row.get("date_id"),
                        new_category, 
                        new_amount, 
                        new_note
                    )
                    if resp.get("status") == "success":
                        st.success("✅ Expense updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update expense.")

        # --- Handle Delete action ---
        if del_btn:
            if "month_category" in row and "date_id" in row:
                resp = delete_expense_from_api(row["month_category"], row["date_id"])
                if resp.get("status") == "success":
                    st.success("🗑️ Expense deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete expense.")
            else:
                st.error("⚠️ Missing keys for deletion — cannot delete this record.")

    # --- Total summary ---
    total = df_full["amount"].sum()
    st.subheader(f"💰 Total Spending: ₹{total:.2f}")

    st.divider()
    st.subheader("📈 Category-wise Summary (Current Month)")

    summary_df = get_category_summary()
    if not summary_df.empty:
        try:
            # st.bar_chart(summary_df.set_index("category")["total"])
            st.dataframe(summary_df, use_container_width=True)
        except Exception as e:
            st.error(f"💥 Error displaying summary: {e}")
    else:
        st.info("No summary data available yet for this month.")