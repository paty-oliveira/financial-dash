import logging

import pandas as pd
import yfinance as yf

logging.basicConfig(filename="YahooFinanceProvider.log", level=logging.ERROR)


class YahooFinance:
    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        stock = yf.Ticker(ticker)
        return stock.isin is not None and len(stock.info) > 1

    @staticmethod
    def get_historical_data(
        ticker: str, columns: [], period: str, interval: str
    ) -> pd.DataFrame:
        stock = yf.Ticker(ticker)
        try:
            return stock.history(period=period, interval=interval)[columns]
        except Exception as e:
            logging.error(
                f"Error fetching historical data from Yahoo Finance for {stock}: {e}"
            )

    @staticmethod
    def get_stock_info(ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        try:
            return stock.info
        except Exception as e:
            logging.error(f"Error fetching stock info for {stock}: {e}")

    @staticmethod
    def get_balance_sheet(ticker: str) -> pd.DataFrame:
        stock = yf.Ticker(ticker)

        try:
            fields = [
                "Current Assets",
                "Current Liabilities",
                "Total Assets",
                "Total Liabilities Net Minority Interest",
                "Total Capitalization",
                "Working Capital",
                "Invested Capital",
                "Total Debt",
                "Net Debt",
                "Stockholders Equity",
            ]

            stock.balance_sheet.loc["Debt to Equity"] = (
                stock.balance_sheet.loc["Total Liabilities Net Minority Interest"]
                / stock.balance_sheet.loc["Stockholders Equity"]
            )
            stock.balance_sheet.loc["Current Ratio"] = (
                stock.balance_sheet.loc["Current Assets"]
                / stock.balance_sheet.loc["Current Liabilities"]
            )

            df_balance_sheet = stock.balance_sheet.transpose()
            df_balance_sheet = df_balance_sheet.reindex(columns=fields, fill_value=0)

            return df_balance_sheet.sort_index().tail(4)
        except Exception as e:
            logging.error(f"Error fetching balance sheet for {stock}: {e}")

    @staticmethod
    def get_income_statement(ticker: str) -> pd.DataFrame:
        stock = yf.Ticker(ticker)

        try:
            fields = [
                "Total Revenue",
                "Cost Of Revenue",
                "Gross Profit",
                "Operating Expense",
                "Operating Income",
                "Total Expenses",
                "Net Income From Continuing Operation Net Minority Interest",
                "EBIT",
                "EBITDA",
                "General And Administrative Expense",
                "Selling And Marketing Expense",
                "Research And Development",
                "Basic EPS",
            ]

            df_income_stmt = stock.income_stmt.transpose()
            df_income_stmt = df_income_stmt.reindex(columns=fields, fill_value=0)

            return df_income_stmt.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching income statement for {stock}: {e}")

    @staticmethod
    def get_cashflow(ticker: str):
        stock = yf.Ticker(ticker)
        try:
            fields = [
                "Operating Cash Flow",
                "Investing Cash Flow",
                "Financing Cash Flow",
                "Capital Expenditure",
                "Free Cash Flow",
            ]
            df_cashflow = stock.cash_flow.transpose()
            df_cashflow = df_cashflow.reindex(columns=fields, fill_value=0)

            return df_cashflow.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching cash flow for {stock}: {e}")
