import streamlit as st


def render(_data_provider):
    data = _data_provider.get_stock_info()
    historical_data = _data_provider.get_historical_data(period="max", interval="1d")[
        "Close"
    ]
    col1, col2 = st.columns(2, gap="large")
    container = st.container()

    with col1:
        st.line_chart(historical_data, x_label="Date", y_label="Price")

    with col2:
        st.write("Placeholder for Company Summary")

    with container:
        st.write(f"{data['longBusinessSummary']}")
