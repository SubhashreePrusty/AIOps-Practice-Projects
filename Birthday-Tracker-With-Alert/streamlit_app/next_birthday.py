import streamlit as st
from itertools import groupby

from api_client import get_birthdays
from utils import next_birthdays


def render_next_birthdays_tab():
    """Display upcoming birthdays."""
    st.subheader("Next Birthdays 🎂")

    def fetch_and_compute_next(n=3):
        records = get_birthdays()

        # Handle if backend returns dict
        if isinstance(records, dict) and "items" in records:
            records = records["items"]

        if not isinstance(records, list):
            st.warning("⚠️ No valid list of birthdays returned from backend.")
            return []

        # Normalize data
        for r in records:
            if "birthday" in r and "date" not in r:
                r["date"] = r["birthday"]

        return next_birthdays(records, count=n)

    next_list = fetch_and_compute_next(n=3)

    if not next_list:
        st.info("No upcoming birthdays found.")
    else:
        # Group by date for neat display
        for next_date, group in groupby(next_list, key=lambda r: r["next_date"]):
            group = list(group)
            st.markdown(f"#### 🎂 {next_date}")
            for rec in group:
                name = rec.get("name", "Unknown")
                age = rec["age_on_next"]
                days = rec["days_left"]
                st.markdown(f"🎈 **{name}** — turning {age} ({days} days left)")
