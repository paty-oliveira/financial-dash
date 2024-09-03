from .yahoo import YahooFinance

YAHOO = "yahoo-finance"


def financial_data_provider(provider_name: str) -> object:
    if provider_name is YAHOO:
        return YahooFinance
    raise ValueError(f"provider_name must be one of {['yahoo-finance']}")
