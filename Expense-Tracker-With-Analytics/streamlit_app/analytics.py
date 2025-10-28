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

    # 🥧 Category-wise Spending Pie Chart
    category_sum = df.groupby("category", as_index=False)["amount"].sum()
    fig1 = px.pie(
        category_sum,
        names="category",
        values="amount",
        title="💸 Spending by Category",
        hole=0.4,  # makes it a donut chart, looks cleaner
        color_discrete_sequence=px.colors.qualitative.Pastel  # soft palette
    )
    
    # Add percentage + amount labels inside the chart
    fig1.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>₹%{value:.2f}<extra></extra>"
    )
    
    st.plotly_chart(fig1, use_container_width=True)

    # 📅 Monthly spending trend
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_sum = df.groupby("month", as_index=False)["amount"].sum()
    fig2 = px.bar(
        monthly_sum,
        x="month",
        y="amount",
        title="📊 Monthly Spending Trend",
        text="amount",
        color="amount",
        color_continuous_scale="purpor"
    )
    
    fig2.update_traces(texttemplate="₹%{text:.2f}", textposition="outside")
    fig2.update_layout(yaxis_title="Amount (₹)", xaxis_title="Month")

    st.plotly_chart(fig2, use_container_width=True)
