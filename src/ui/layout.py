import streamlit as st

from .raw_content import homepage_content, footer_content, not_found_ticker_content


def render(financial_data, financial_calculations):
    ticker = st.session_state["ticker"]
    if not ticker:
        render_homepage()
    elif not financial_data.is_valid_ticker(ticker):
        render_invalid_ticker_placeholder()
    else:
        render_stock_info(financial_data, financial_calculations)
        render_footer()


def render_homepage():
    st.markdown(homepage_content, unsafe_allow_html=True)


def render_invalid_ticker_placeholder():
    st.markdown(not_found_ticker_content, unsafe_allow_html=True)


def render_footer():
    st.markdown(footer_content, unsafe_allow_html=True)


def render_stock_info(financial_data, financial_calculations):
    # Render header
    render_header(financial_data, financial_calculations)
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


def render_header(financial_data, financial_calculations):
    stock_info = financial_data.get_stock_info(
        st.session_state["ticker"],
    )
    ticker = stock_info["symbol"]
    company_name = stock_info["longName"]
    st.markdown(f"### {ticker} - {company_name}", unsafe_allow_html=True)
    # Render price change
    current_price = stock_info["currentPrice"]
    previous_close_price = stock_info["previousClose"]
    currency = stock_info["currency"]
    currency_symbol = financial_calculations["currency_symbol"](currency)
    current_price_content = f"{currency_symbol}{current_price}"
    price_diff = financial_calculations["price_changes"](
        current_price, previous_close_price
    )
    price_diff_content = f"({price_diff}%)"
    price_change_content = (
        apply_text_color(price_diff_content, "red")
        if price_diff < 0
        else apply_text_color(price_diff_content, "green")
    )
    st.markdown(
        f"#####  {current_price_content} {price_change_content}",
        unsafe_allow_html=True,
    )


def render_overview(financial_data):
    ticker = st.session_state["ticker"]
    historical_data = financial_data.get_historical_data(
        ticker,
        columns=["Close"],
        period="max",
        interval="1d",
    )
    quotes = financial_data.get_stock_info(ticker)
    stock_performance, ratios_summary = st.columns(2, gap="large")

    with stock_performance:
        st.markdown("#### Stock Performance")
        st.line_chart(historical_data, x_label="Date", y_label="Price")

    with ratios_summary:
        st.markdown("#### Price and Market Data")
        properties, values = st.columns(2)
        with properties:
            st.write("Previous Close")
            st.write("Open")
            st.write("Day High")
            st.write("Day Low")
            st.write("Bid")
            st.write("Ask")
            st.write("Volume")
            st.write("Market Cap")

        with values:
            st.write(f" **{quotes['previousClose']:,}**")
            st.write(f" **{quotes['open']:,}**")
            st.write(f" **{quotes['dayHigh']:,}**")
            st.write(f" **{quotes['dayLow']:,}**")
            st.write(f" **{quotes['bid']:,} x {quotes['bidSize']}**")
            st.write(f" **{quotes['ask']:,} x {quotes['askSize']}**")
            st.write(f" **{quotes['volume']:,}**")
            st.write(f" **{quotes['marketCap']:,}**")

    with st.container():
        st.markdown("#### Company Profile")
        st.expander("Business Summary").write(quotes["longBusinessSummary"])
        st.expander("Sector").markdown(
            f" [{quotes['sector']}](https://finance.yahoo.com/sectors/{quotes['sectorKey'].lower()}) "
        )
        st.expander("Industry").markdown(
            f" [{quotes['industry']}](https://finance.yahoo.com/sectors/{quotes['sectorKey'].lower()}/{quotes['industryKey'].lower()}) "
        )
        st.expander("Country").write(quotes["country"])
        st.expander("Website").write(quotes["website"])


def render_balance_sheet(financial_data):
    balance_sheet = financial_data.get_balance_sheet(st.session_state["ticker"])
    st.dataframe(balance_sheet)


def render_income_stmt(financial_data):
    income_stmt = financial_data.get_income_statement(st.session_state["ticker"])
    st.dataframe(income_stmt)


def render_cashflow(financial_data):
    cashflow = financial_data.get_cashflow(st.session_state["ticker"])
    st.dataframe(cashflow)


def apply_text_color(text, color):
    return f"<span style='color:{color}'>{text}</span>"
