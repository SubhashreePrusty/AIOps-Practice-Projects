# app.py
import streamlit as st
from add_expense import show_add_expense
from view_expenses import show_view_expenses
from analytics import show_analytics

st.set_page_config(page_title="Expense Tracker with Analytics 💰", layout="centered")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Add Expense", "View Expenses", "Analytics"])

st.title("💸📈 Expense Tracker")
st.write("This application helps you track your expenses.")

st.markdown("""
#### Features:
- Add, view, edit and delete expenses.
- Category-wise summaries, analytics-charts.
""")

if page == "Add Expense":
    show_add_expense()
elif page == "View Expenses":
    show_view_expenses()
else:
    show_analytics()

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + AWS Lambda + DynamoDB -- by Sayonika, Samiksha, and Pratik!")