from .currency import convert_currency_symbol
from .financial_formulas import calculate_price_changes

financial_calculations = {
    "currency_symbol": convert_currency_symbol,
    "price_changes": calculate_price_changes,
}
