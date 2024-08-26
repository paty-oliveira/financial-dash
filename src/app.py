import streamlit as st

from components import sidebar, container

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    container.render()
    sidebar.render()


main()
