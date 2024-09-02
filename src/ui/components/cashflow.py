import streamlit as st


def render(_data_provider):
    df = _data_provider.get_cash_flow()
    st.dataframe(df)
