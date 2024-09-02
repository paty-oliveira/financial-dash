import streamlit as st


def render(_data_provider):
    st.write("Income Statement tab")
    df = _data_provider.get_income_statement()
    st.dataframe(df)
