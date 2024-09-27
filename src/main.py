import os

import toml

import core
import infra
import ui

_financial_provider = None
_financial_calculations = None


def initialize_financial_provider(provider_name):
    global _financial_provider
    if _financial_provider is None:
        _financial_provider = infra.financial_data_provider(provider_name)


def initialize_financial_formulas():
    global _financial_calculations
    if _financial_calculations is None:
        _financial_calculations = core.financial_calculations


def main():
    configs = toml.load(os.path.abspath("config.toml"))
    initialize_financial_provider(infra.YAHOO)
    initialize_financial_formulas()
    ui.run(_financial_provider, _financial_calculations, configs)


if __name__ == "__main__":
    main()
