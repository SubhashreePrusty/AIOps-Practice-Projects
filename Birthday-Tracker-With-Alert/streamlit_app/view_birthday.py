import streamlit as st
import json

from api_client import get_birthdays, delete_birthday

def render_view_birthdays_tab():
    st.subheader("All Saved Birthdays")
    birthdays = get_birthdays()
    
    # Parse if nested 'body'
    if isinstance(birthdays, dict) and "body" in birthdays and isinstance(birthdays["body"], str):
        birthdays = json.loads(birthdays["body"])

    # Handle error or empty case
    if "error" in birthdays:
        st.error(f"⚠️ {birthdays['error']}")
        return
    elif not birthdays.get("items"):
        st.info("No birthdays found yet! Add some first 👆")
        return

    # ✅ Sort by name alphabetically (case-insensitive)
    sorted_birthdays = sorted(birthdays["items"], key=lambda x: x["name"].lower())

    # Display all birthdays
    for idx, b in enumerate(sorted_birthdays):
        col1, col2 = st.columns([3, 1])  # columns: name/birthday | delete

        # Show name and birthday
        col1.write(f"**{b['name']}** 🎈 — {b['birthday']}")

        # Delete button
        with col2:
            delete_key = f"del_{b['name']}_{b['birthday']}"

            if st.button("Delete", key=delete_key):
                response = delete_birthday(b['name'], b['birthday'])
                if "error" in response:
                    st.error(response["error"])
                else:
                    st.success(response.get("message", "Birthday deleted successfully!"))
                    st.rerun()
