import streamlit as st
import pandas as pd
from utils import get_all_expenses, get_category_summary
from edit_expense import edit_expense_form
from delete_expense import handle_delete_expense


def show_view_expenses():
    st.header("📊 View & Manage Expenses")

    df_full = get_all_expenses()

    if df_full.empty:
        st.warning("No expenses found yet. Add some!")
        return

    # ✅ Keep backend keys but show only necessary columns
    expected_cols = ["date", "category", "amount", "note", "month_category", "date_id"]
    df_full = df_full[[c for c in expected_cols if c in df_full.columns]]

    st.write("### 💸 Expense List")

    # ✅ Table headers
    header_cols = st.columns([2, 2, 2, 3, 1, 1])
    headers = ["Date", "Category", "Amount", "Note", "Edit", "Delete"]
    for col, name in zip(header_cols, headers):
        col.markdown(f"**{name}**")

    # ✅ Track which expense is being edited
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

    # ✅ Loop through each expense row
    for i, row in df_full.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])

        col1.write(row.get("date", "-"))
        col2.write(row.get("category", "-"))
        col3.write(f"₹{row.get('amount', 0):.2f}")
        col4.write(row.get("note", "-"))

        edit_btn = col5.button("✏️", key=f"edit_{i}")
        del_btn = col6.button("🗑️", key=f"del_{i}")

        # ✅ When edit button clicked, store which item is being edited
        if edit_btn:
            st.session_state.edit_index = i

        # ✅ Show edit form for the selected index
        if st.session_state.edit_index == i:
            edit_expense_form(row, i)

        if del_btn:
            handle_delete_expense(row)

    # --- Summary ---
    total = df_full["amount"].sum()
    st.subheader(f"💰 Total Spending: ₹{total:.2f}")

    st.divider()
    st.subheader("📈 Category-wise Summary (Current Month)")

    summary_df = get_category_summary()
    if not summary_df.empty:
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.info("No summary data available yet for this month.")
