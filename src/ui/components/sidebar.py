import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


def render():
    with st.sidebar:
        st.title("Dashboard :bar_chart:")
        st.text_input("Enter a stock ticker:", key="ticker", type="default")
        button(username="devpatrici0", floating=True)
