import streamlit as st

from ..utils.markdown import read_file


def render():
    homepage_file = "src/ui/content/homepage.md"
    homepage_content = read_file(homepage_file)
    st.markdown(homepage_content, unsafe_allow_html=True)
