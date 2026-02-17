def calculate_position(entry, stop, risk_per_trade=100):
    risk_per_share = abs(entry - stop)

    if risk_per_share == 0:
        return {"error": "Entry and stop cannot be the same."}

    position_size = risk_per_trade / risk_per_share
    target_2r = entry + (entry - stop) * 2
    target_3r = entry + (entry - stop) * 3

    return {
        "position_size": round(position_size, 0),
        "2R_target": round(target_2r, 2),
        "3R_target": round(target_3r, 2)
    }
