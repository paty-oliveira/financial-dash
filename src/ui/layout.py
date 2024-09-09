import plotly.graph_objects as go
import streamlit as st

from .raw_content import homepage_content, footer_content, not_found_ticker_content
from .styling import apply_text_color, apply_tag_style


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
        columns=["Close", "Open", "High", "Low"],
        period="max",
        interval="1d",
    )
    quotes = financial_data.get_stock_info(ticker)
    stock_performance, ratios_summary = st.columns(2, gap="large")

    with stock_performance:
        st.markdown("#### Stock Performance")
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=historical_data.index,
                    open=historical_data["Open"],
                    high=historical_data["High"],
                    low=historical_data["Low"],
                    close=historical_data["Close"],
                )
            ]
        )
        fig.update_layout(
            xaxis_rangeslider_visible=False, xaxis_title="Date", yaxis_title="Price"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    with ratios_summary:
        st.markdown("#### Price and Market Data")
        properties_text = [
            "Previous Close",
            "Open",
            "Day High",
            "Day Low",
            "Volume",
            "Market Cap",
            "Beta",
            "PE Ratio",
            "EPS",
            "Forward Dividend & Yield",
        ]
        values_text = [
            f"**{quotes['previousClose']:,}**",
            f"**{quotes['open']:,}**",
            f"**{quotes['dayHigh']:,}**",
            f"**{quotes['dayLow']:,}**",
            f"**{quotes['volume']:,}**",
            f"**{quotes['marketCap']:,}**",
            f"**{quotes['beta']:.3}**",
            f"**{quotes['trailingPE']:.4}**",
            f"**{quotes['trailingEps']:.3}**",
            (
                f"**{quotes['dividendRate']:.2} ({quotes['dividendYield'] * 100:.2}%)**"
                if "dividendRate" in quotes
                else "0"
            ),
        ]
        properties, values = st.columns(2)
        with properties:
            for content in properties_text:
                st.write(content)

        with values:
            for content in values_text:
                st.write(content)

    with st.container():
        st.markdown("#### Company Profile")
        st.write(quotes["longBusinessSummary"])

        sector_key = quotes["sectorKey"].lower()
        sector_content = apply_tag_style(
            f"https://finance.yahoo.com/sectors/{sector_key}", quotes["sector"]
        )

        industry_key = quotes["industryKey"].lower()
        industry_content = apply_tag_style(
            f"https://finance.yahoo.com/sectors/{sector_key}/{industry_key}",
            quotes["industry"],
        )

        website_content = apply_tag_style(quotes["website"], "Website")

        st.markdown(
            f"""
                <div class='tags-container'>
                    {sector_content}
                    {industry_content}
                    {website_content}
                </div>
            """,
            unsafe_allow_html=True,
        )


def render_balance_sheet(financial_data):
    balance_sheet = financial_data.get_balance_sheet(st.session_state["ticker"])
    st.dataframe(balance_sheet)


def render_income_stmt(financial_data):
    income_stmt = financial_data.get_income_statement(st.session_state["ticker"])
    st.dataframe(income_stmt)


def render_cashflow(financial_data):
    cashflow = financial_data.get_cashflow(st.session_state["ticker"])
    st.dataframe(cashflow)
