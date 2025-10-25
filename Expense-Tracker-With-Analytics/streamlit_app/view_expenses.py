# View / visualize expenses page

# view_expenses.py
import streamlit as st
from utils import get_all_expenses

def show_view_expenses():
    st.header("📊 View All Expenses")
    df = get_all_expenses()

    if df.empty:
        st.warning("No expenses found yet. Add some!")
        return

    st.dataframe(df)

    total = df["amount"].sum()
    st.subheader(f"💰 Total Spending: ₹{total:.2f}")
