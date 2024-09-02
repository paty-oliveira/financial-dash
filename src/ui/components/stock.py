from .content import render as content
from .footer import render as footer
from .header import render as header


def render(_data_provider):
    header(_data_provider)
    content(_data_provider)
    footer()
