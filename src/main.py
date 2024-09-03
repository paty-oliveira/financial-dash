import infra
import ui

_financial_provider = None


def initialize_financial_provider(provider_name):
    global _financial_provider
    if _financial_provider is None:
        _financial_provider = infra.financial_data_provider(provider_name)


def main():
    initialize_financial_provider(infra.YAHOO)
    ui.run(_financial_provider)


if __name__ == "__main__":
    main()
