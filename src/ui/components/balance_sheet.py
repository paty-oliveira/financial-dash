import streamlit as st


def render(_data_provider):
    df = _data_provider.get_balance_sheet()
    st.dataframe(df)
