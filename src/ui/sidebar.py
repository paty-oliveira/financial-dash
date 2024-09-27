import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


def render(feedback_form_url):
    with st.sidebar:
        st.title("Dashboard :bar_chart:")
        st.text_input("Enter a stock ticker:", key="ticker", type="default")
        button(username="devpatrici0", floating=True)

        with st.container():
            st.write("### We would love your feedback!")
            st.markdown(" Click the link below to access the feedback form.")
            st.markdown(
                f"""
                <a href="{feedback_form_url}" target="_blank">
                    <button class="feedback-btn">
                        Submit Feedback
                    </button>
                </a>
                """,
                unsafe_allow_html=True,
            )
