import streamlit as st


def render():
    with st.sidebar:
        st.title("Dashboard :bar_chart:")
        st.text_input("Enter a stock ticker:", key="ticker", type="default")
