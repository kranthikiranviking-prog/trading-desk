def calculate_regime(df):

    if df.empty:
        return 0

    latest = df.iloc[-1]

    score = 0

    # EMA Structure
    if latest["ema20"] > latest["ema50"]:
        score += 40

    # Price above VWAP
    if latest["close"] > latest["vwap"]:
        score += 30

    # RSI momentum
    if latest["rsi"] > 55:
        score += 30

    return score

