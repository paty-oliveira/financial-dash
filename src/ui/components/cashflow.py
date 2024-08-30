import streamlit as st


@st.cache_data
def render(_data_provider):
    df = _data_provider.get_cash_flow()
    st.dataframe(df)
