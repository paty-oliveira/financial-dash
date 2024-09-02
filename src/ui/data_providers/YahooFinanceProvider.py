import logging
from abc import ABC

import pandas as pd
import yfinance as yf

from .FinancialDataProvider import FinancialDataProvider

logging.basicConfig(filename="YahooFinanceProvider.log", level=logging.ERROR)


class YahooFinanceProvider(FinancialDataProvider, ABC):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.stock = yf.Ticker(ticker)
        self.general_info = self.stock.info
        self.balance_sheet = self.stock.balance_sheet
        self.income_stmt = self.stock.income_stmt
        self.cash_flow = self.stock.cash_flow

    def get_historical_data(self, period: str, interval: str) -> pd.DataFrame:
        try:
            return self.stock.history(period=period, interval=interval)
        except Exception as e:
            logging.error(
                f"Error fetching historical data from Yahoo Finance for {self.stock}: {e}"
            )

    def get_stock_info(self) -> dict:
        try:
            return self.general_info
        except Exception as e:
            logging.error(f"Error fetching stock info for {self.stock}: {e}")

    def get_balance_sheet(self) -> pd.DataFrame:
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

            self.balance_sheet.loc["Debt to Equity"] = (
                self.balance_sheet.loc["Total Liabilities Net Minority Interest"]
                / self.balance_sheet.loc["Stockholders Equity"]
            )
            self.balance_sheet.loc["Current Ratio"] = (
                self.balance_sheet.loc["Current Assets"]
                / self.balance_sheet.loc["Current Liabilities"]
            )

            df_balance_sheet = self.balance_sheet.transpose()
            df_balance_sheet = df_balance_sheet.reindex(columns=fields, fill_value=0)

            return df_balance_sheet.sort_index().tail(4)
        except Exception as e:
            logging.error(f"Error fetching balance sheet for {self.stock}: {e}")

    def get_income_statement(self) -> pd.DataFrame:
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

            df_income_stmt = self.income_stmt.transpose()
            df_income_stmt = df_income_stmt.reindex(columns=fields, fill_value=0)

            return df_income_stmt.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching income statement for {self.stock}: {e}")

    def get_cash_flow(self):
        try:
            fields = [
                "Operating Cash Flow",
                "Investing Cash Flow",
                "Financing Cash Flow",
                "Capital Expenditure",
                "Free Cash Flow",
            ]
            df_cashflow = self.cash_flow.transpose()
            df_cashflow = df_cashflow.reindex(columns=fields, fill_value=0)

            return df_cashflow.sort_index().tail(4)

        except Exception as e:
            logging.error(f"Error fetching cash flow for {self.stock}: {e}")
