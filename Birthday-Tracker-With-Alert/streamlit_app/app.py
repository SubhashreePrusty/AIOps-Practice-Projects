import streamlit as st
import datetime

from api_client import add_birthday
from utils import format_birthday, is_future_date

st.title("🎂 Birthday Tracker")
st.subheader("This application helps you track birthdays of your friends and send alerts.")

st.markdown("""
### Features:
- Add, view, and manage birthdays.
- Receive alerts for upcoming birthdays.
- User-friendly interface.
""")


name = st.text_input("Enter name:")
date = st.date_input(
    "Enter birthday:",
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date(2100, 12, 31)
)

# Validate input
if is_future_date(date):
    st.error("❌ Birthday cannot be in the future!")

if st.button("Save"):
    formatted_date = format_birthday(date)
    response = add_birthday(name, formatted_date)
    st.success(response.get("message", "Birthday added!"))