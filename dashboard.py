import streamlit as st
import pandas as pd

st.title("Driver Drowsiness Dashboard")

try:
    st.write("Loading trip_stats.csv...")
    stats = pd.read_csv("trip_stats.csv")
    st.success("trip_stats.csv loaded")

    st.write("Loading alert_logs.csv...")
    logs = pd.read_csv("alert_logs.csv")
    st.success("alert_logs.csv loaded")

    st.write(stats)
    st.write(logs)

except Exception as e:
    st.error(f"ERROR: {e}")