def calculate_price_changes(current_price, previous_close_price, decimal_point=2):
    return (
        round(
            (current_price - previous_close_price) / previous_close_price, decimal_point
        )
        * 100
    )
