import streamlit as st
import pandas as pd
import os

# Import our existing analysis logic
from database.connection import engine
from src.analysis import load_accidents_df, severity_distribution, time_summary, location_summary

st.set_page_config(page_title="Road Accident Dashboard", layout="wide")

st.title("🚗 Road Accident Data Analysis Dashboard")
st.markdown("> **Note:** Associations only — not proof of causation. Synthetic data used.")

# Load data
@st.cache_data
def get_data():
    return load_accidents_df(engine)

try:
    df = get_data()
    
    if df.empty:
        st.warning("No data found. Please run `python main.py all --rows 800` in your terminal first.")
    else:
        # --- Top Metrics ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Accidents", len(df))
        col2.metric("Fatal Accidents", len(df[df['severity'] == 'Fatal']))
        col3.metric("Regions Covered", df['region'].nunique())
        col4.metric("Vehicle Types", df['vehicle_type'].nunique())

        st.divider()

        # --- Charts ---
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Severity Distribution")
            st.bar_chart(severity_distribution(df).set_index("severity")["count"])
            
            st.subheader("Accidents by Day of Week")
            days = time_summary(df)["by_day_of_week"]
            st.bar_chart(days.set_index("day_of_week")["count"])

        with col_right:
            st.subheader("Top 10 Regions")
            reg = location_summary(df).groupby("region")["count"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(reg)
            
            st.subheader("Accidents by Hour of Day")
            hours = time_summary(df)["by_hour"]
            st.line_chart(hours.set_index("hour")["count"])

        # --- Raw Data ---
        st.divider()
        st.subheader("Raw Data Sample")
        st.dataframe(df.head(50))

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure you have run `python main.py all` first to generate the database.")