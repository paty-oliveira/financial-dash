import streamlit as st


@st.cache_data
def render(_data_provider):
    st.write("Income Statement tab")
    df = _data_provider.get_income_statement()
    st.dataframe(df)
