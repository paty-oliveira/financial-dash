import logging
from typing import Literal

import pandas as pd
import yfinance as yf

logging.basicConfig(filename="YahooFinanceProvider.log", level=logging.ERROR)


class YahooFinance:
    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        stock = yf.Ticker(ticker)
        return len(stock.info) > 1

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
    def get_balance_sheet(
        ticker: str, frequency: Literal["yearly", "quarterly"]
    ) -> pd.DataFrame:
        stock = yf.Ticker(ticker)

        balance_sheet = (
            stock.balance_sheet
            if frequency == "yearly"
            else stock.quarterly_balance_sheet
        )

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

            balance_sheet.loc["Debt to Equity"] = (
                balance_sheet.loc["Total Liabilities Net Minority Interest"]
                / balance_sheet.loc["Stockholders Equity"]
            )
            balance_sheet.loc["Current Ratio"] = (
                balance_sheet.loc["Current Assets"]
                / balance_sheet.loc["Current Liabilities"]
            )

            df_balance_sheet = balance_sheet.transpose()
            df_balance_sheet = df_balance_sheet.reindex(columns=fields, fill_value=0)

            return df_balance_sheet.sort_index().tail(4)
        except Exception as e:
            logging.error(f"Error fetching balance sheet for {stock}: {e}")

    @staticmethod
    def get_income_statement(
        ticker: str, frequency: Literal["yearly", "quarterly"]
    ) -> pd.DataFrame:
        stock = yf.Ticker(ticker)

        income_statement = (
            stock.income_stmt if frequency == "yearly" else stock.quarterly_income_stmt
        )

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

            df_income_stmt = income_statement.transpose()
            df_income_stmt = df_income_stmt.reindex(columns=fields, fill_value=0)

            return df_income_stmt.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching income statement for {stock}: {e}")

    @staticmethod
    def get_cashflow(
        ticker: str, frequency: Literal["yearly", "quarterly"]
    ) -> pd.DataFrame:
        stock = yf.Ticker(ticker)

        cashflow = (
            stock.cash_flow if frequency == "yearly" else stock.quarterly_cashflow
        )

        try:
            fields = [
                "Operating Cash Flow",
                "Investing Cash Flow",
                "Financing Cash Flow",
                "Capital Expenditure",
                "Free Cash Flow",
            ]
            df_cashflow = cashflow.transpose()
            df_cashflow = df_cashflow.reindex(columns=fields, fill_value=0)

            return df_cashflow.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching cash flow for {stock}: {e}")
