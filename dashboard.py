import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
import os
import matplotlib.pyplot as plt

stats_file = "stats.json"
cumul_stats_file = "cumul_stats.json"

def load_stats(filename):
    """
    Loads moderation statistics from the given JSON file if it exists.
    Returns: dict or None (the parsed JSON statistics if the file exists, otherwise None).
    """
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        return json.load(f)

def plot_bar_chart(data, xlabel, ylabel, sort_desc=True):
    """
    Plots a matplotlib bar chart with customizable font size.
    """
    if isinstance(data, dict):
        labels = list(data.keys())
        values = list(data.values())
        # Sort by value descending (default)
        if sort_desc:
            sorted_items = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
            labels, values = zip(*sorted_items)
        fig, ax = plt.subplots()
        bars = ax.bar(labels, values)
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        # Add headroom
        ax.set_ylim(0, max(values) * 1.15)
        # Add value labels on top of each bar
        ax.bar_label(bars, padding=3, fontsize=12)
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.bar_chart(data)

def main():
    st.title("Real-Time Moderation Analytics Dashboard")
    # Auto-refresh every 2 seconds (2000 ms)
    st_autorefresh(interval=2000, key="datarefresh")
    stats = load_stats(stats_file)
    cumul_stats = load_stats(cumul_stats_file)

    if stats:
        st.header("Number of Reviews by Decision (Session)")
        plot_bar_chart(stats["decision_counts"], xlabel="Decision", ylabel="Number of Reviews")
        st.header("Number of Reviews by Business (Session)")
        plot_bar_chart(stats["business_counts"], xlabel="Business", ylabel="Number of Reviews")
        st.header("Number of Reviews by User (Session)")
        plot_bar_chart(stats["user_counts"], xlabel="User", ylabel="Number of Reviews")
        st.write(f"Total Events Processed (Session): {stats['event_count']}")
    else:
        st.info("No session stats available yet. Waiting for data...")

    if cumul_stats:
        st.header("Number of Reviews by Decision (Cumulative)")
        plot_bar_chart(cumul_stats["decision_counts"], xlabel="Decision", ylabel="Number of Reviews")
        st.header("Number of Reviews by Business (Cumulative)")
        plot_bar_chart(cumul_stats["business_counts"], xlabel="Business", ylabel="Number of Reviews")
        st.header("Number of Reviews by User (Cumulative)")
        plot_bar_chart(cumul_stats["user_counts"], xlabel="User", ylabel="Number of Reviews")
        st.write(f"Total Events Processed (Cumulative): {cumul_stats['event_count']}")
    else:
        st.info("No cumulative stats available yet. Waiting for data...")

if __name__ == "__main__":
    main()