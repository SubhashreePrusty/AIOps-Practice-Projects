import streamlit as st
import datetime

from api_client import add_birthday
from utils import format_birthday, is_future_date
from next_birthday import render_next_birthdays_tab
from view_birthday import render_view_birthdays_tab

st.title("🎂 Birthday Tracker")
st.write("This application helps you track birthdays of your friends and send alerts.")

st.markdown("""
### Features:
- Add, view, and delete birthdays.
- Receive email alerts (11:00pm IST) for upcoming birthdays and (9:00am IST) for current birthdays.
""")

# --- Initialize session state ---
if "name_input" not in st.session_state:
    st.session_state.name_input = ""
if "date_input" not in st.session_state:
    st.session_state.date_input = datetime.date.today()
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# --- Reset logic BEFORE widgets render ---
if st.session_state.reset_form:
    st.session_state.name_input = ""
    st.session_state.date_input = datetime.date.today()
    st.session_state.reset_form = False

# --- Widgets ---
name = st.text_input("Enter name:", key="name_input")
date = st.date_input(
    "Enter birthday:",
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date(2100, 12, 31),
    key="date_input"
)

# --- Validation ---
if is_future_date(date):
    st.error("❌ Birthday cannot be in the future!")

# --- Button action ---
if st.button("➕ Add Birthday"):
    formatted_date = format_birthday(date)
    response = add_birthday(name, formatted_date)

    if "error" in response:
        st.error(f"⚠️ {response['error']}")
    else:
        st.success("✅ Birthday added successfully!")

        # ✅ Instead of direct overwrite, set reset flag
        st.session_state.reset_form = True
        st.rerun()


tab1, tab2 = st.tabs(["🎂 Next Birthday", "📅 View Birthdays"])

with tab1:
    render_next_birthdays_tab()

with tab2:
    render_view_birthdays_tab()

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + AWS Lambda + DynamoDB + SNS -- by Subhashree, Shaily, and Pratik!")