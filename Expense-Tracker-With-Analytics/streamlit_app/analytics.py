# insights/charts

# analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_all_expenses

def show_analytics():
    st.header("📈 Expense Analytics")

    df = get_all_expenses()
    if df.empty:
        st.warning("No data available for analytics.")
        return

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Category-wise spending
    category_sum = df.groupby("category")["amount"].sum().reset_index()
    fig1 = px.pie(category_sum, names="category", values="amount", title="Spending by Category")
    st.plotly_chart(fig1)

    # Monthly spending trend
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_sum = df.groupby("month")["amount"].sum().reset_index()
    fig2 = px.bar(monthly_sum, x="month", y="amount", title="Monthly Spending Trend")
    st.plotly_chart(fig2)