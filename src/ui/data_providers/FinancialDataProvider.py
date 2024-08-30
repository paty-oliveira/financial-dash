from abc import ABC, abstractmethod

import pandas as pd


class FinancialDataProvider(ABC):
    def __init__(self, ticker: str):
        self.ticker = ticker

    @abstractmethod
    def get_historical_data(self, period: str, interval: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_stock_info(self) -> dict:
        pass

    @abstractmethod
    def get_balance_sheet(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_income_statement(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_cash_flow(self) -> pd.DataFrame:
        pass
