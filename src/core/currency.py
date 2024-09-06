def convert_currency_symbol(currency_symbol):
    currency = {
        "USD": "$",  # US Dollar
        "EUR": "€",  # Euro
        "JPY": "¥",  # Japanese Yen
        "GBP": "£",  # British Pound Sterling
        "AUD": "A$",  # Australian Dollar
        "CAD": "C$",  # Canadian Dollar
        "CHF": "CHF",  # Swiss Franc
        "CNY": "¥",  # Chinese Yuan Renminbi
        "HKD": "HK$",  # Hong Kong Dollar
        "INR": "₹",  # Indian Rupee
        "RUB": "₽",  # Russian Ruble
        "BRL": "R$",  # Brazilian Real
        "ZAR": "R",  # South African Rand
        "KRW": "₩",  # South Korean Won
        "MXN": "$",  # Mexican Peso
        "SGD": "S$",  # Singapore Dollar
        "NZD": "NZ$",  # New Zealand Dollar
        "TRY": "₺",  # Turkish Lira
        "SEK": "kr",  # Swedish Krona
        "NOK": "kr",  # Norwegian Krone
    }

    return currency[currency_symbol]
