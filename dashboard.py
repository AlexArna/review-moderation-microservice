import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
import os


stats_file = "stats.json"

def load_stats():
    """
    Loads moderation statistics from the stats.json file if it exists.
    Returns: dict or None (the parsed JSON statistics if the file exists, otherwise None).
    """
    if not os.path.exists(stats_file):
        return None
    with open(stats_file, "r") as f:
        return json.load(f)

def main():
    st.title("Real-Time Moderation Analytics Dashboard")
    # Auto-refresh every 2 seconds (2000 ms)
    st_autorefresh(interval=2000, key="datarefresh")
    stats = load_stats()
    if stats:
        st.header("Moderation Decision Counts")
        st.bar_chart(stats["decision_counts"])
        st.header("Counts per Business")
        st.bar_chart(stats["business_counts"])
        st.header("Counts per User")
        st.bar_chart(stats["user_counts"])
        st.write(f"Total Events Processed: {stats['event_count']}")
    else:
        st.info("No stats available yet. Waiting for data...")

if __name__ == "__main__":
    main()
