import streamlit as st


@st.cache_data
def render(_data_provider):
    data = _data_provider.get_stock_info()
    st.json(data)
