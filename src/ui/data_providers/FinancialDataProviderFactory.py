from .YahooFinanceProvider import YahooFinanceProvider


class FinancialDataProviderFactory:
    def __init__(self, ticker: str, provider_name: str = "yahoo-finance", **kwargs):
        self.provider_name = provider_name
        self.ticker = ticker
        self.kwargs = kwargs

    def get_provider(self):
        return YahooFinanceProvider(self.ticker)
