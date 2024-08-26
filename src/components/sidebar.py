import streamlit as st


def on_change():
    if "ticker" not in st.session_state:
        st.session_state["ticker"] = ""
    st.session_state["ticker"] = st.session_state["ticker"]


def display():
    st.sidebar.title("Stock Screener")
    st.sidebar.text_input(
        label="Introduce a valid Ticker:",
        placeholder="Ticker",
        key="ticker",
        on_change=on_change,
    )
