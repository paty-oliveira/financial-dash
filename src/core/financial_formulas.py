def calculate_percentage_value_change(current_value, previous_value):
    return ((current_value - previous_value) / previous_value) * 100


def calculate_value_diff(current_value, previous_value):
    return current_value - previous_value


def calculate_debt_equity(total_liabilities, stockholder_equity):
    return total_liabilities / stockholder_equity


def calculate_current_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities
