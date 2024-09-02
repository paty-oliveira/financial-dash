from .footer import render as footer
from .header import render as header
from .tabs import render as tabs


def render(_data_provider):
    header(_data_provider)
    tabs(_data_provider)
    footer()
