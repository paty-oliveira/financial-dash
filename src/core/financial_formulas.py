def calculate_price_changes(current_price, previous_close_price):
    return round((current_price - previous_close_price) / previous_close_price, 2) * 100
