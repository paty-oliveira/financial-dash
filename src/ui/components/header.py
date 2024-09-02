import streamlit as st


def render(_data_provider):
    data = _data_provider.get_stock_info()

    st.markdown(f"### {data['symbol']} - {data['longName']}", unsafe_allow_html=True)
