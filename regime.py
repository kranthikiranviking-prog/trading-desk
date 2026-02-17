def classify_regime(df):
    latest = df.iloc[-1]

    score = 0

    if latest['close'] > latest['ema20']:
        score += 25
    if latest['ema20'] > latest['ema50']:
        score += 25
    if latest['rvol'] > 1.2:
        score += 25
    if latest['rsi'] > 50:
        score += 25

    if score >= 70:
        regime = "Trend"
    elif score <= 40:
        regime = "Range"
    else:
        regime = "Neutral"

    return score, regime
