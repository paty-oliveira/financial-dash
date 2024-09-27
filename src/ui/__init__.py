import streamlit as st
import streamlit.components.v1 as components

from .layout import render as render_layout
from .sidebar import render as render_sidebar
from .stylesheet import global_stylesheet

initial_state = {"ticker": "", "balance_sheet_frequency": "yearly"}


def run(financial_data, financial_calculations, configs):
    feedback_form_url = configs["general"]["feedback_form_url"]
    contribution_url = configs["general"]["contribution_url"]

    st.set_page_config(
        page_title="Stock Analysis Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add Google Analytics Tracking
    with open("src/ui/google_analytics.html", "r") as f:
        html_code = f.read()
        components.html(html_code, height=0)

    # Injecting global CSS stylesheet
    st.markdown(global_stylesheet, unsafe_allow_html=True)

    # Creating Session State
    for k, v in initial_state.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # performs the rendering
    render_layout(financial_data, financial_calculations)
    render_sidebar(feedback_form_url, contribution_url)
