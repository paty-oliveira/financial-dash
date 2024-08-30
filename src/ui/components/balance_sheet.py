import streamlit as st


@st.cache_data
def render(_data_provider):
    df = _data_provider.get_balance_sheet()
    st.dataframe(df)
