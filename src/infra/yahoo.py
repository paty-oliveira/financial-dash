import logging
from typing import Literal

import pandas as pd
import yfinance as yf

logging.basicConfig(filename="YahooFinanceProvider.log", level=logging.ERROR)


class YahooFinance:
    NUMBER_ROWS = 4

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
            df_balance_sheet = balance_sheet.transpose()
            df_balance_sheet.index = pd.DatetimeIndex(df_balance_sheet.index).date

            return df_balance_sheet.sort_index().tail(YahooFinance.NUMBER_ROWS)
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
            df_income_stmt = income_statement.transpose()
            df_income_stmt.index = pd.DatetimeIndex(df_income_stmt.index).date

            return df_income_stmt.sort_index().tail(YahooFinance.NUMBER_ROWS)

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
            df_cashflow = cashflow.transpose()
            df_cashflow.index = pd.DatetimeIndex(df_cashflow.index).date

            return df_cashflow.sort_index().tail(YahooFinance.NUMBER_ROWS)

        except Exception as e:
            logging.error(f"Error fetching cash flow for {stock}: {e}")
