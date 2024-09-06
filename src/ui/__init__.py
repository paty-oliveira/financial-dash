import streamlit as st

from .layout import render as render_layout
from .sidebar import render as render_sidebar

initial_state = {"ticker": ""}


def run(financial_data, financial_calculations):
    st.set_page_config(
        page_title="Stock Analysis Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    for k, v in initial_state.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # performs the rendering
    render_layout(financial_data, financial_calculations)
    render_sidebar()
