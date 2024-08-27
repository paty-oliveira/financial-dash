import streamlit as st


def render():
    with st.sidebar:
        st.title("Dashboard")
        st.text_input("Write a valid Ticker", key="ticker", type="default")
