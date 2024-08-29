import streamlit as st

from ..utils.markdown import read_file


def render():
    footer_file = "src/ui/content/footer.md"
    footer_content = read_file(footer_file)
    st.markdown(footer_content, unsafe_allow_html=True)
