from .footer import render as footer
from .homepage import render as homepage
from .stock import render as stock
from ..data_providers.FinancialDataProviderFactory import FinancialDataProviderFactory
from ..state import Ticker


def render():
    ticker = Ticker()

    if ticker.is_available():
        ticker_name = ticker.get_ticker()
        data_provider = FinancialDataProviderFactory(ticker_name).get_provider()
        stock(data_provider)
        footer()

    else:
        homepage()
