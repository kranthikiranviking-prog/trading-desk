# live_ws.py

import os
from alpaca.data.live import StockDataStream
from institutional_engine import rolling_bars, evaluate_breakout, latest_prices


def start_stream():

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    stream = StockDataStream(
        api_key,
        secret_key,
        feed="iex"   # FREE FEED
    )

    async def on_bar(bar):
        symbol = bar.symbol

        data = {
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
        }

        rolling_bars[symbol].append(data)
        latest_prices[symbol] = bar.close

        evaluate_breakout(symbol)

    stream.subscribe_bars(on_bar, "TSLA", "NVDA", "SPY", "QQQ")

    stream.run()

