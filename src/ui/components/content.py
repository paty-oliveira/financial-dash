import streamlit as st

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

    tabs = st.tabs(options)
    for tab, (tab_name, content) in zip(tabs, tab_content.items()):
        with tab:
            content(_data_provider)
