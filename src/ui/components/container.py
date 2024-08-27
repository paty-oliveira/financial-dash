import streamlit as st
import streamlit_shadcn_ui as ui

from .balance_sheet_tab import render as balance_sheet
from .cashflow_tab import render as cashflow
from .income_stmt_tab import render as income_stmt
from .overview_tab import render as overview
from ..state import Ticker

tab_content = {
    "Overview": overview,
    "Balance Sheet": balance_sheet,
    "Income Statement": income_stmt,
    "CashFlow": cashflow,
}


def render():
    ticker_name = Ticker()

    if ticker_name.is_available():
        options = list(tab_content.keys())
        current_tab = ui.tabs(options, default_value=options[0], key="current_tab")
        return tab_content[current_tab]()

    else:
        st.write("welcome page")
        st.write("Write a valid ticker to start your analysis!")
