import ta


def calculate_indicators(df):

    if df.empty:
        return df

    df["ema20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)

    # Relative Volume
    df["rvol"] = df["volume"] / df["volume"].rolling(20).mean()

    # VWAP
    df["vwap"] = (
        (df["volume"] * (df["high"] + df["low"] + df["close"]) / 3).cumsum()
        / df["volume"].cumsum()
    )

    return df

