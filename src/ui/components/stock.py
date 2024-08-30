import streamlit_shadcn_ui as ui

from .balance_sheet import render as balance_sheet
from .cashflow import render as cashflow
from .income_stmt import render as income_stmt
from .overview import render as overview

tab_content = {
    "Overview": overview,
    "Balance Sheet": balance_sheet,
    "Income Statement": income_stmt,
    "CashFlow": cashflow,
}


def render(_data_provider):
    options = list(tab_content.keys())
    current_tab = ui.tabs(options, default_value=options[0], key="current_tab")

    return tab_content[current_tab](_data_provider)
