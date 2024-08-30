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
            fields = [
                "country",
                "industry",
                "sector",
                "longBusinessSummary",
                "symbol",
                "longName",
                "trailingPE",
                "dividendYield",
                "payoutRatio",
                "trailingEps",
                "returnOnAssets",
                "returnOnEquity",
                "marketCap",
                "operatingCashflow",
            ]

            return {
                key: self.general_info[key]
                for key in fields
                if key in self.general_info
            }
        except Exception as e:
            logging.error(f"Error fetching stock info for {self.stock}: {e}")

    def get_balance_sheet(self) -> pd.DataFrame:
        try:
            self.balance_sheet.loc["Debt to Equity"] = (
                self.balance_sheet.loc["Total Liabilities Net Minority Interest"]
                / self.balance_sheet.loc["Stockholders Equity"]
            )
            self.balance_sheet.loc["Current Ratio"] = (
                self.balance_sheet.loc["Current Assets"]
                / self.balance_sheet.loc["Current Liabilities"]
            )

            return self.balance_sheet
        except Exception as e:
            logging.error(f"Error fetching balance sheet for {self.stock}: {e}")

    def get_income_statement(self) -> pd.DataFrame:
        try:
            return self.income_stmt

        except Exception as e:
            logging.error(f"Error fetching income statement for {self.stock}: {e}")

    def get_cash_flow(self):
        try:
            return self.cash_flow

        except Exception as e:
            logging.error(f"Error fetching cash flow for {self.stock}: {e}")
