import streamlit as st


class Ticker:
    def __init__(self):
        if "ticker" not in st.session_state:
            st.session_state["ticker"] = ""
        self.name = st.session_state["ticker"]

    def get_ticker(self):
        return self.name.upper()

    def is_available(self):
        return self.name != ""
