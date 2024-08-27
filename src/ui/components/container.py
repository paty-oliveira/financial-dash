from .homepage import render as homepage
from .stock import render as stock
from ..state import Ticker


def render():
    ticker_name = Ticker()

    if ticker_name.is_available():
        return stock()

    else:
        return homepage()
