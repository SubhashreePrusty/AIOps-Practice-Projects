# app.py
import streamlit as st
from add_expense import show_add_expense
from view_expenses import show_view_expenses
from analytics import show_analytics

st.set_page_config(page_title="Expense Tracker with Analytics 💰", layout="centered")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Add Expense", "View Expenses", "Analytics"])

if page == "Add Expense":
    show_add_expense()
elif page == "View Expenses":
    show_view_expenses()
else:
    show_analytics()
