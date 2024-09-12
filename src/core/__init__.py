from .currency import convert_currency_symbol
from .financial_formulas import (
    calculate_percentage_value_change,
    calculate_value_diff,
    calculate_debt_equity,
    calculate_current_ratio,
)

financial_calculations = {
    "currency_symbol": convert_currency_symbol,
    "percentage_value_change": calculate_percentage_value_change,
    "value_diff": calculate_value_diff,
    "debt_equity": calculate_debt_equity,
    "current_ratio": calculate_current_ratio,
}
