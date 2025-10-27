import streamlit as st
import datetime
import json
from api_client import add_birthday, get_birthdays, delete_birthday
from utils import format_birthday, is_future_date

st.title("🎂 Birthday Tracker")
st.write("This application helps you track birthdays of your friends and send alerts.")

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

if st.button("➕ Add Birthday"):
    formatted_date = format_birthday(date)
    response = add_birthday(name, formatted_date)
    if "error" in response:
        st.error(f"⚠️ {response['error']}")
    else:
        st.success("Birthday added successfully!")

tab1, tab2 = st.tabs(["🎂 Next Birthday", "📅 View Birthdays"])

with tab1:
    st.subheader("Next Birthday -- Coming Soon!")
    st.info("No birthdays found yet! Add some first 👆")

with tab2:
    st.subheader("All Saved Birthdays")
    birthdays = get_birthdays()
    
    # Parse if nested 'body'
    if isinstance(birthdays, dict) and "body" in birthdays and isinstance(birthdays["body"], str):
        birthdays = json.loads(birthdays["body"])

    if "error" in birthdays:
        st.error(f"⚠️ {birthdays['error']}")
    elif birthdays.get("items"):
        for idx, b in enumerate(birthdays["items"]):
            col1, col2 = st.columns([3, 2])  # columns: name/birthday | delete

            # Show name and birthday
            col1.write(f"**{b['name']}** 🎈 — {b['birthday']}")

            # Delete button
            with col2:
                delete_key = f"del_{b['name']}_{b['birthday']}"

                if st.button(f"Delete", key=delete_key):
                    response = delete_birthday(b['name'], b['birthday'])
                    if "error" in response:
                        st.error(response["error"])
                    else:
                        st.success(response.get("message", "Birthday deleted successfully!"))
                        st.rerun()  # updated from experimental_rerun
    else:
        st.info("No birthdays found yet! Add some first 👆")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + AWS Lambda + DynamoDB + SNS -- by Subhashree, Shaily, and Pratik!")