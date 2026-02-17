def calculate_position_size(account_size, risk_percent, stop_distance):

    if stop_distance <= 0:
        return 0

    risk_amount = account_size * (risk_percent / 100)

    position_size = risk_amount / stop_distance

    return position_size

