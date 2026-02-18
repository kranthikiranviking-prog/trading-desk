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

