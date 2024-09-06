import streamlit as st

from .raw_content import homepage_content, footer_content, not_found_ticker_content


def render(financial_data):
    ticker = st.session_state["ticker"]
    if not ticker:
        render_homepage()
    elif not financial_data.is_valid_ticker(ticker):
        render_invalid_ticker_placeholder()
    else:
        render_stock_info(financial_data)
        render_footer()


def render_homepage():
    st.markdown(homepage_content, unsafe_allow_html=True)


def render_invalid_ticker_placeholder():
    st.markdown(not_found_ticker_content, unsafe_allow_html=True)


def render_footer():
    st.markdown(footer_content, unsafe_allow_html=True)


def render_stock_info(financial_data):
    # Render header
    render_header(financial_data)
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


def render_header(financial_data):
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
    current_price_content = f"{convert_currency_symbol(currency)}{current_price}"
    price_diff = calculate_price_changes(current_price, previous_close_price)
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
        st.markdown("#### Summary")
        st.write("Placeholder for Company Summary")

    with st.container():
        st.markdown("#### Company Profile")
        company_summary_expander = st.expander("Business Summary")
        company_summary_expander.write(quotes["longBusinessSummary"])
        # sector
        # industry
        # employees
        # founded year
        # Country
        # Currency
        # website
        # (?) logo


def render_balance_sheet(financial_data):
    balance_sheet = financial_data.get_balance_sheet(st.session_state["ticker"])
    st.dataframe(balance_sheet)


def render_income_stmt(financial_data):
    income_stmt = financial_data.get_income_statement(st.session_state["ticker"])
    st.dataframe(income_stmt)


def render_cashflow(financial_data):
    cashflow = financial_data.get_cashflow(st.session_state["ticker"])
    st.dataframe(cashflow)


def convert_currency_symbol(currency_symbol):
    currency = {
        "USD": "$",  # US Dollar
        "EUR": "€",  # Euro
        "JPY": "¥",  # Japanese Yen
        "GBP": "£",  # British Pound Sterling
        "AUD": "A$",  # Australian Dollar
        "CAD": "C$",  # Canadian Dollar
        "CHF": "CHF",  # Swiss Franc
        "CNY": "¥",  # Chinese Yuan Renminbi
        "HKD": "HK$",  # Hong Kong Dollar
        "INR": "₹",  # Indian Rupee
        "RUB": "₽",  # Russian Ruble
        "BRL": "R$",  # Brazilian Real
        "ZAR": "R",  # South African Rand
        "KRW": "₩",  # South Korean Won
        "MXN": "$",  # Mexican Peso
        "SGD": "S$",  # Singapore Dollar
        "NZD": "NZ$",  # New Zealand Dollar
        "TRY": "₺",  # Turkish Lira
        "SEK": "kr",  # Swedish Krona
        "NOK": "kr",  # Norwegian Krone
    }

    return currency[currency_symbol]


def calculate_price_changes(current_price, previous_close_price):
    return round((current_price - previous_close_price) / previous_close_price, 2) * 100


def apply_text_color(text, color):
    return f"<span style='color:{color}'>{text}</span>"
