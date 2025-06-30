import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
import os
import matplotlib.pyplot as plt

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

def plot_bar_chart(data, xlabel, ylabel):
    """
    Plots a matplotlib bar chart with customizable font size.
    """
    if isinstance(data, dict):
        labels = list(data.keys())
        values = list(data.values())
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.bar_chart(data)

def main():
    st.title("Real-Time Moderation Analytics Dashboard")
    # Auto-refresh every 2 seconds (2000 ms)
    st_autorefresh(interval=2000, key="datarefresh")
    stats = load_stats()
    if stats:
        st.header("Number of Reviews by Decision")
        plot_bar_chart(stats["decision_counts"], xlabel="Decision", ylabel="Number of Reviews")
        st.header("Number of Reviews by Business")
        plot_bar_chart(stats["business_counts"], xlabel="Business", ylabel="Number of Reviews")
        st.header("Number of Reviews by User")
        plot_bar_chart(stats["user_counts"], xlabel="User", ylabel="Number of Reviews")
        st.write(f"Total Events Processed: {stats['event_count']}")
    else:
        st.info("No stats available yet. Waiting for data...")

if __name__ == "__main__":
    main()