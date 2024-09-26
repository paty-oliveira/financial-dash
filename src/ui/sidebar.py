import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


def render():
    with st.sidebar:
        st.title("Dashboard :bar_chart:")
        st.text_input("Enter a stock ticker:", key="ticker", type="default")
        button(username="devpatrici0", floating=True)

        with st.container():
            st.write("### We would love your feedback!")
            st.text_input("Name:", key="username", type="default")
            st.text_input("Email:", key="user_email", type="default")
            # user_feedback = st.text_area(
            #     "Please provide your suggestions or feedback here:",
            #     key="feedback",
            # )
            # app_rating = st.feedback("stars")
            st.button("Submit", type="primary", use_container_width=True)
