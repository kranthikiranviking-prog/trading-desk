# institutional_engine.py

from collections import deque
import pandas as pd

MAX_BARS = 200

rolling_bars = {
    "TSLA": deque(maxlen=MAX_BARS),
    "NVDA": deque(maxlen=MAX_BARS),
    "SPY": deque(maxlen=MAX_BARS),
    "QQQ": deque(maxlen=MAX_BARS),
}

latest_signal = {}
latest_prices = {}


def calculate_ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()


def calculate_vwap(df):
    cum_vol = df["volume"].cumsum()
    cum_vol_price = (df["close"] * df["volume"]).cumsum()
    return cum_vol_price / cum_vol


def evaluate_breakout(symbol):
    bars = rolling_bars[symbol]

    if len(bars) < 25:
        return None

    df = pd.DataFrame(bars)

    df["ema20"] = calculate_ema(df["close"])
    df["vwap"] = calculate_vwap(df)
    df["avg_vol"] = df["volume"].rolling(20).mean()

    last = df.iloc[-1]
    prev5_high = df["high"].iloc[-6:-1].max()
    prev5_low = df["low"].iloc[-6:-1].min()

    conditions = [
        last["close"] > prev5_high,
        last["volume"] > 2 * last["avg_vol"],
        last["close"] > last["ema20"],
        last["close"] > last["vwap"],
        last["close"] > last["open"],
    ]

    if all(conditions):

        entry = last["close"]
        stop = prev5_low
        risk_per_share = entry - stop

        if risk_per_share <= 0:
            return None

        shares = int(500 / risk_per_share)
        target = entry + 2 * risk_per_share

        signal = {
            "symbol": symbol,
            "type": "Breakout Continuation",
            "entry": round(entry, 2),
            "stop": round(stop, 2),
            "shares": shares,
            "target": round(target, 2),
        }

        latest_signal[symbol] = signal
        return signal

    return None

