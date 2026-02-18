# live_ws.py

import os
import asyncio
from alpaca.data.live import StockDataStream
from institutional_engine import rolling_bars, evaluate_breakout

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

symbols = ["TSLA", "NVDA", "SPY"]

stream = StockDataStream(API_KEY, SECRET_KEY)


async def on_bar(bar):
    symbol = bar.symbol

    if symbol not in rolling_bars:
        return

    rolling_bars[symbol].append({
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume,
        "timestamp": bar.timestamp,
    })

    signal = evaluate_breakout(symbol)

    if signal:
        print("🚨 SIGNAL DETECTED:", signal)


def start_stream():
    for symbol in symbols:
        stream.subscribe_bars(on_bar, symbol)

    stream.run()

