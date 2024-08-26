import streamlit as st

from components import sidebar

st.set_page_config(
    page_title="Financial Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

sidebar.display()
