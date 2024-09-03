import streamlit as st

from .raw_content import homepage_content, footer_content


def render(financial_data):
    ticker = st.session_state["ticker"]
    if not ticker:
        render_homepage()
    elif not financial_data.is_valid_ticker(ticker):
        st.write("Invalid ticker")
    else:
        render_stock_info(financial_data)
        render_footer()


def render_homepage():
    st.markdown(homepage_content, unsafe_allow_html=True)


def render_footer():
    st.markdown(footer_content, unsafe_allow_html=True)


def render_stock_info(financial_data):
    stock_info = financial_data.get_stock_info(
        st.session_state["ticker"],
    )
    # Render header
    st.markdown(
        f"### {stock_info['symbol']} - {stock_info['longName']}", unsafe_allow_html=True
    )
    # Renders tabs
    tab_titles = ["Overview", "Balance Sheet", "Income Statement", "CashFlow"]
    tabs_renderings = [
        render_overview,
        render_balance_sheet,
        render_income_stmt,
        render_cashflow,
    ]
    st_tabs = st.tabs(tab_titles)
    for tab, render_action in zip(st_tabs, tabs_renderings):
        with tab:
            render_action(financial_data)


def render_overview(financial_data):
    ticker = st.session_state["ticker"]
    historical_data = financial_data.get_historical_data(
        ticker,
        columns=["Close"],
        period="max",
        interval="1d",
    )
    quotes = financial_data.get_stock_info(ticker)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.line_chart(historical_data, x_label="Date", y_label="Price")

    with col2:
        st.write("Placeholder for Company Summary")

    with st.container():
        st.write(f"{quotes['longBusinessSummary']}")


def render_balance_sheet(financial_data):
    balance_sheet = financial_data.get_balance_sheet(st.session_state["ticker"])
    st.dataframe(balance_sheet)


def render_income_stmt(financial_data):
    income_stmt = financial_data.get_income_statement(st.session_state["ticker"])
    st.dataframe(income_stmt)


def render_cashflow(financial_data):
    cashflow = financial_data.get_cashflow(st.session_state["ticker"])
    st.dataframe(cashflow)
