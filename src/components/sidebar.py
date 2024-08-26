import streamlit as st

import streamlit_shadcn_ui as ui


def render():
    with st.sidebar:
        st.title("Dashboard")
        ui.input(placeholder="Write a valid Ticker", type="text", key="ticker")
