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
            render_action(financial_data, financial_calculations)


def render_header(financial_data, financial_calculations):
    stock_info = financial_data.get_stock_info(
        st.session_state["ticker"],
    )
    st.markdown(
        f"### {stock_info['symbol']} - {stock_info['longName']}", unsafe_allow_html=True
    )
    # Render price change
    current_price = float(stock_info["currentPrice"])
    previous_close_price = float(stock_info["previousClose"])
    currency_symbol = financial_calculations["currency_symbol"](stock_info["currency"])
    current_price_content = f"{currency_symbol}{current_price:.2f}"
    price_diff = financial_calculations["percentage_value_change"](
        current_price, previous_close_price
    )
    price_diff_content = f"({price_diff:.2f}%)"
    price_change_content = (
        apply_text_color(price_diff_content, "red")
        if price_diff < 0
        else apply_text_color(price_diff_content, "green")
    )
    st.markdown(
        f"#####  {current_price_content} {price_change_content}",
        unsafe_allow_html=True,
    )


def render_overview(financial_data, *kwargs):
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


def render_balance_sheet(financial_data, financial_calculations, frequency="yearly"):
    balance_sheet = financial_data.get_balance_sheet(
        st.session_state["ticker"], frequency=frequency
    )

    with st.container():
        col1, col2, col3 = st.columns(3)

        current_total_assets = int(balance_sheet["Total Assets"][0])
        previous_total_assets = int(balance_sheet["Total Assets"][1])
        total_assets_diff = financial_calculations["value_diff"](
            current_total_assets, previous_total_assets
        )
        total_assets_change = financial_calculations["percentage_value_change"](
            current_total_assets, previous_total_assets
        )
        col1.metric(
            label="Total Assets",
            value=f"{current_total_assets:,}",
            delta=f"{total_assets_diff:,} ({total_assets_change:.2f}%)",
        )

        current_total_liabilities = int(
            balance_sheet["Total Liabilities Net Minority Interest"][0]
        )
        previous_total_liabilities = int(
            balance_sheet["Total Liabilities Net Minority Interest"][1]
        )
        total_liabilities_diff = financial_calculations["value_diff"](
            current_total_liabilities, previous_total_liabilities
        )
        total_liabilities_change = financial_calculations["percentage_value_change"](
            current_total_liabilities, previous_total_liabilities
        )
        col2.metric(
            label="Total Liabilities",
            value=f"{current_total_liabilities:,}",
            delta=f"{total_liabilities_diff:,} ({total_liabilities_change:.2f}%)",
            delta_color="inverse",
        )

        current_working_capital = int(balance_sheet["Working Capital"][0])
        previous_working_capital = int(balance_sheet["Working Capital"][1])
        working_capital_diff = financial_calculations["value_diff"](
            current_working_capital, previous_working_capital
        )
        working_capital_change = financial_calculations["percentage_value_change"](
            current_working_capital, previous_working_capital
        )
        col3.metric(
            label="Working Capital",
            value=f"{current_working_capital:,}",
            delta=f"{working_capital_diff:,} ({working_capital_change:.2f}%)",
        )

        with st.container():
            col1, col2, col3 = st.columns(3)

            current_debt = int(balance_sheet["Total Debt"][0])
            previous_debt = int(balance_sheet["Total Debt"][1])
            total_debt_diff = financial_calculations["value_diff"](
                current_debt, previous_debt
            )
            total_debt_change = financial_calculations["percentage_value_change"](
                current_debt, previous_debt
            )
            col1.metric(
                label="Total Debt",
                value=f"{current_debt:,}",
                delta=f"{total_debt_diff:,} ({total_debt_change:.2f})%",
                delta_color="inverse",
            )

            current_debt_equity = financial_calculations["debt_equity"](
                float(balance_sheet["Total Liabilities Net Minority Interest"][0]),
                float(balance_sheet["Stockholders Equity"][0]),
            )
            previous_debt_equity = financial_calculations["debt_equity"](
                float(balance_sheet["Total Liabilities Net Minority Interest"][1]),
                float(balance_sheet["Stockholders Equity"][1]),
            )
            debt_equity_diff = financial_calculations["value_diff"](
                current_debt_equity, previous_debt_equity
            )
            debt_equity_change = financial_calculations["percentage_value_change"](
                current_debt_equity, previous_debt_equity
            )
            col2.metric(
                label="Debt to Equity",
                value=f"{current_debt_equity:.3}",
                delta=f"{debt_equity_diff:.2} ({debt_equity_change:.2f}%)",
                delta_color="inverse",
            )

            current_ratio = financial_calculations["current_ratio"](
                float(balance_sheet["Current Assets"][0]),
                float(balance_sheet["Current Liabilities"][1]),
            )

            previous_ratio = financial_calculations["current_ratio"](
                float(balance_sheet["Current Assets"][1]),
                float(balance_sheet["Current Liabilities"][1]),
            )
            current_ratio_diff = financial_calculations["value_diff"](
                current_ratio, previous_ratio
            )
            current_ratio_change = financial_calculations["percentage_value_change"](
                current_ratio, previous_ratio
            )
            col3.metric(
                label="Current Ratio",
                value=f"{current_ratio:.3}",
                delta=f"{current_ratio_diff:.3} ({current_ratio_change:.2f}%)",
            )


def render_income_stmt(financial_data, *kwargs):
    income_stmt = financial_data.get_income_statement(
        st.session_state["ticker"], frequency="quarterly"
    )
    st.dataframe(income_stmt)


def render_cashflow(financial_data, *kwargs):
    cashflow = financial_data.get_cashflow(
        st.session_state["ticker"], frequency="quarterly"
    )
    st.dataframe(cashflow)
