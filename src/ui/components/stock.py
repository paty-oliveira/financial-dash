from .content import render as content
from .header import render as header


def render(_data_provider):
    header(_data_provider)
    content(_data_provider)
