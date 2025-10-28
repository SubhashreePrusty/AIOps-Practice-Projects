
# view_expenses.py
import streamlit as st
from utils import get_all_expenses, get_category_summary

def show_view_expenses():
    st.header("📊 View All Expenses")

    df = get_all_expenses()

    if df.empty:
        st.warning("No expenses found yet. Add some!")
        return

    st.dataframe(df, use_container_width=True)

    total = df["amount"].sum()
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