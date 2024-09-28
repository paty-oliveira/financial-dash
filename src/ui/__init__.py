import os
import pathlib

import streamlit as st
from bs4 import BeautifulSoup

from .layout import render as render_layout
from .sidebar import render as render_sidebar
from .stylesheet import global_stylesheet

initial_state = {"ticker": "", "balance_sheet_frequency": "yearly"}


def run(financial_data, financial_calculations):
    feedback_form_url = os.getenv("FEEDBACK_FORM_URL")
    donation_url = os.getenv("DONATION_URL")
    ga_tracking_id = os.getenv("GA_TRACKING_ID")

    st.set_page_config(
        page_title="Stock Analysis Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add Google Analytics Tracking
    google_analytics_content = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_tracking_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];

            function gtag() {{
                dataLayer.push(arguments);
            }}

            gtag('js', new Date());

            gtag('config', {ga_tracking_id});
        </script>
    """
    # Insert the script in the head tag of the static template inside your virtual environment
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), "lxml")

    if not soup.find(id="ga-script"):
        script_tag = soup.new_tag("script", id="ga-script")
        script_tag.string = google_analytics_content
        soup.head.append(script_tag)
        index_path.write_text(str(soup))

    # Injecting global CSS stylesheet
    st.markdown(global_stylesheet, unsafe_allow_html=True)

    # Creating Session State
    for k, v in initial_state.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # performs the rendering
    render_layout(financial_data, financial_calculations)
    render_sidebar(feedback_form_url, donation_url)
