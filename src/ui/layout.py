import plotly.graph_objects as go
import streamlit as st
from streamlit_pills import pills

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
            f"**{float(quotes['previousClose']):.2f}**",
            f"**{float(quotes['open']):.2f}**",
            f"**{float(quotes['dayHigh']):.2f}**",
            f"**{float(quotes['dayLow']):.2f}**",
            f"**{int(quotes['volume']):,}**",
            f"**{int(quotes['marketCap']):,}**",
            f"**{float(quotes['beta']):.2f}**",
            f"**{float(quotes['trailingPE']):.2f}**",
            f"**{float(quotes['trailingEps']):.2f}**",
            (
                f"**{float(quotes['dividendRate']):.2f} ({float(quotes['dividendYield']) * 100:.2f}%)**"
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


report_frequency_mapping = {
    "Annual": "yearly",
    "Quarterly": "quarterly",
}


def render_balance_sheet(financial_data, financial_calculations):
    frequency = pills(
        "Select report frequency:",
        ["Annual", "Quarterly"],
        key="frequency_balance_sheet",
    )

    balance_sheet = financial_data.get_balance_sheet(
        st.session_state["ticker"], frequency=report_frequency_mapping[frequency]
    )

    # Render Metrics
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
                delta=f"{total_debt_diff:,} ({total_debt_change:.2f}%)",
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

        st.divider()

        # Render Charts
        with st.container():
            assets_liabilities_chart, total_debt_chart = st.columns(2)

            with assets_liabilities_chart:
                fig = go.Figure(
                    data=[
                        go.Bar(
                            x=balance_sheet.index,
                            y=balance_sheet["Total Assets"].values,
                            name="Total Assets",
                            marker_color="forestgreen",
                            marker=dict(cornerradius="5%"),
                        ),
                        go.Bar(
                            x=balance_sheet.index,
                            y=balance_sheet[
                                "Total Liabilities Net Minority Interest"
                            ].values,
                            name="Total Liabilities",
                            marker_color="tomato",
                            marker=dict(cornerradius="5%"),
                        ),
                    ]
                )
                fig.update_layout(
                    xaxis=dict(type="category"),
                    title="Assets vs Liabilities",
                )
                st.plotly_chart(fig, use_container_width=True)

            with total_debt_chart:
                fig = go.Figure(
                    data=[
                        go.Bar(
                            x=balance_sheet.index,
                            y=balance_sheet["Total Debt"].values,
                            name="Total Debt",
                            marker_color="tomato",
                            marker=dict(cornerradius="5%"),
                            width=0.4,
                        )
                    ]
                )
                fig.update_layout(
                    xaxis=dict(type="category"), title="Total Debt Evolution"
                )
                st.plotly_chart(fig, use_container_width=True)

    with st.container():
        invested_capital, working_capital = st.columns(2)

        with invested_capital:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=balance_sheet.index,
                        y=balance_sheet["Invested Capital"].values,
                        name="Invested Capital",
                        marker_color="forestgreen",
                        marker=dict(cornerradius="5%"),
                        width=0.4,
                    )
                ]
            )
            fig.update_layout(
                xaxis=dict(type="category"), title="Invested Capital Evolution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with working_capital:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=balance_sheet.index,
                        y=balance_sheet["Working Capital"].values,
                        name="Working Capital",
                        marker_color="dodgerblue",
                        marker=dict(cornerradius="5%"),
                        width=0.4,
                    )
                ]
            )
            fig.update_layout(
                xaxis=dict(type="category"), title="Working Capital Evolution"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Render Balance Sheet Overview
    with st.container():
        st.markdown("#### Balance Sheet Overview")
        st.write("Hover over the table to download it as a CSV file")
        st.dataframe(balance_sheet)


def render_income_stmt(financial_data, financial_calculations):
    frequency = pills(
        "Select report frequency:",
        ["Annual", "Quarterly"],
        key="frequency_income_stmt",
    )

    income_stmt = financial_data.get_income_statement(
        st.session_state["ticker"], frequency=report_frequency_mapping[frequency]
    )

    # Render metrics
    with st.container():
        col1, col2, col3 = st.columns(3)

        current_total_revenue = int(income_stmt["Total Revenue"][0])
        previous_total_revenue = int(income_stmt["Total Revenue"][1])
        total_revenue_diff = financial_calculations["value_diff"](
            current_total_revenue, previous_total_revenue
        )
        total_revenue_change = financial_calculations["percentage_value_change"](
            current_total_revenue, previous_total_revenue
        )
        col1.metric(
            label="Total Revenue",
            value=f"{current_total_revenue:,}",
            delta=f"{total_revenue_diff:,} ({total_revenue_change:.2f}%)",
        )

        current_cost_revenue = int(income_stmt["Cost Of Revenue"][0])
        previous_cost_revenue = int(income_stmt["Cost Of Revenue"][1])
        cost_revenue_diff = financial_calculations["value_diff"](
            current_cost_revenue, previous_cost_revenue
        )
        cost_revenue_change = financial_calculations["percentage_value_change"](
            current_cost_revenue, previous_cost_revenue
        )
        col2.metric(
            label="Cost Of Revenue",
            value=f"{current_cost_revenue:,}",
            delta=f"{cost_revenue_diff:,} ({cost_revenue_change:.2f}%)",
            delta_color="inverse",
        )

        current_gross_profit = int(income_stmt["Gross Profit"][0])
        previous_gross_profit = int(income_stmt["Gross Profit"][1])
        gross_profit_diff = financial_calculations["value_diff"](
            current_gross_profit, previous_gross_profit
        )
        gross_profit_change = financial_calculations["percentage_value_change"](
            current_gross_profit, previous_gross_profit
        )
        col3.metric(
            label="Gross Profit",
            value=f"{current_gross_profit:,}",
            delta=f"{gross_profit_diff:,} ({gross_profit_change:.2f}%)",
        )

    with st.container():
        col1, col2, col3 = st.columns(3)

        current_operating_income = int(income_stmt["Operating Income"][0])
        previous_operating_income = int(income_stmt["Operating Income"][1])
        operating_income_diff = financial_calculations["value_diff"](
            current_operating_income, previous_operating_income
        )
        operating_income_change = financial_calculations["percentage_value_change"](
            current_operating_income, previous_operating_income
        )
        col1.metric(
            label="Operating Income",
            value=f"{current_operating_income:,}",
            delta=f"{operating_income_diff:,} ({operating_income_change:.2f}%)",
        )

        current_operating_expense = int(income_stmt["Operating Expense"][0])
        previous_operating_expense = int(income_stmt["Operating Expense"][1])
        operating_expense_diff = financial_calculations["value_diff"](
            current_operating_expense, previous_operating_expense
        )
        operating_expense_change = financial_calculations["percentage_value_change"](
            current_operating_expense, previous_operating_expense
        )
        col2.metric(
            label="Operating Expense",
            value=f"{current_operating_expense:,}",
            delta=f"{operating_expense_diff:,} ({operating_expense_change:.2f}%)",
            delta_color="inverse",
        )

        current_total_expenses = int(income_stmt["Total Expenses"][0])
        previous_total_expenses = int(income_stmt["Total Expenses"][1])
        total_expenses_diff = financial_calculations["value_diff"](
            current_total_expenses, previous_total_expenses
        )
        total_expenses_change = financial_calculations["percentage_value_change"](
            current_total_expenses, previous_total_expenses
        )
        col3.metric(
            label="Total Expenses",
            value=f"{current_total_expenses:,}",
            delta=f"{total_expenses_diff:,} ({total_expenses_change:.2f}%)",
            delta_color="inverse",
        )

    with st.container():
        col1, col2, col3 = st.columns(3)

        current_net_income = int(income_stmt["Net Income"][0])
        previous_net_income = int(income_stmt["Net Income"][1])
        net_income_diff = financial_calculations["value_diff"](
            current_net_income, previous_net_income
        )
        net_income_change = financial_calculations["percentage_value_change"](
            current_net_income, previous_net_income
        )
        col1.metric(
            label="Net Income",
            value=f"{current_net_income:,}",
            delta=f"{net_income_diff:,} ({net_income_change:.2f}%)",
        )

        current_eps = float(income_stmt["Diluted EPS"][0])
        previous_eps = float(income_stmt["Diluted EPS"][1])
        eps_diff = financial_calculations["value_diff"](current_eps, previous_eps)
        eps_change = financial_calculations["percentage_value_change"](
            current_eps, previous_eps
        )
        col2.metric(
            label="Earnings Per Share (EPS)",
            value=f"{current_eps:.2f}",
            delta=f"{eps_diff:.2f} ({eps_change:.2f}%)",
        )

        current_ebitda = int(income_stmt["EBITDA"][0])
        previous_ebitda = int(income_stmt["EBITDA"][1])
        ebitda_diff = financial_calculations["value_diff"](
            current_ebitda, previous_ebitda
        )
        ebitda_change = financial_calculations["percentage_value_change"](
            current_ebitda, previous_ebitda
        )
        col3.metric(
            label="Earnings Before Interest, Taxes, Depreciation and Amortisation (EBITDA)",
            value=f"{current_ebitda:,}",
            delta=f"{ebitda_diff:,} ({ebitda_change:.2f}%)",
        )

    st.divider()

    # Render Charts
    with st.container():
        income, expenses = st.columns(2)

        with income:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=income_stmt.index,
                        y=income_stmt["Net Income"].values,
                        name="Net Income",
                        marker_color="mediumseagreen",
                        marker=dict(cornerradius="5%"),
                    ),
                    go.Bar(
                        x=income_stmt.index,
                        y=income_stmt["Operating Income"].values,
                        name="Operating Income",
                        marker_color="forestgreen",
                        marker=dict(cornerradius="5%"),
                    ),
                ]
            )
            fig.update_layout(
                xaxis=dict(type="category"),
                title="Net Income vs Operating Income",
            )
            st.plotly_chart(fig, use_container_width=True)

        with expenses:
            if {"Selling And Marketing Expense", "Research And Development"}.issubset(
                income_stmt.columns
            ):
                fig = go.Figure(
                    data=[
                        go.Bar(
                            x=income_stmt.index,
                            y=income_stmt["General And Administrative Expense"].values,
                            name="Administrative Expense",
                            marker_color="dodgerblue",
                            marker=dict(cornerradius="5%"),
                            width=0.6,
                        ),
                        go.Bar(
                            x=income_stmt.index,
                            y=income_stmt["Selling And Marketing Expense"].values,
                            name="Marketing Expense",
                            marker_color="lightskyblue",
                            marker=dict(cornerradius="5%"),
                            width=0.6,
                        ),
                        go.Bar(
                            x=income_stmt.index,
                            y=income_stmt["Research And Development"].values,
                            name="Research Expense",
                            marker_color="steelblue",
                            marker=dict(cornerradius="5%"),
                            width=0.6,
                        ),
                    ]
                )
                fig.update_layout(
                    xaxis=dict(type="category"),
                    title="Expenses Breakdown",
                    barmode="stack",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = go.Figure(
                    data=[
                        go.Bar(
                            x=income_stmt.index,
                            y=income_stmt["Total Expenses"].values,
                            name="Total Expenses",
                            marker_color="tomato",
                            marker=dict(cornerradius="5%"),
                            width=0.4,
                        )
                    ]
                )
                fig.update_layout(
                    xaxis=dict(type="category"),
                    title="Total Expenses Evolution",
                    barmode="stack",
                )
                st.plotly_chart(fig, use_container_width=True)

    with st.container():
        eps, ebitda = st.columns(2)

        with eps:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=income_stmt.index,
                        y=income_stmt["Diluted EPS"].values,
                        name="EPS",
                        marker_color="forestgreen",
                        marker=dict(cornerradius="5%"),
                        width=0.4,
                    )
                ]
            )
            fig.update_layout(xaxis=dict(type="category"), title="EPS Evolution")
            st.plotly_chart(fig, use_container_width=True)

        with ebitda:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=income_stmt.index,
                        y=income_stmt["EBITDA"].values,
                        name="EBITDA",
                        marker_color="dodgerblue",
                        marker=dict(cornerradius="5%"),
                        width=0.4,
                    )
                ]
            )
            fig.update_layout(xaxis=dict(type="category"), title="EBITDA Evolution")
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Render Income Statement Overview
    st.markdown("#### Income Statement Overview")
    st.write("Hover over the table to download it as a CSV file")
    st.dataframe(income_stmt)


def render_cashflow(financial_data, *kwargs):
    frequency = pills(
        "Select report frequency:",
        ["Annual", "Quarterly"],
        key="frequency_cashflow",
    )

    cashflow = financial_data.get_cashflow(
        st.session_state["ticker"], frequency=report_frequency_mapping[frequency]
    )

    st.markdown("#### Cashflow Overview")
    st.write("Hover over the table to download it as a CSV file")
    st.dataframe(cashflow)
