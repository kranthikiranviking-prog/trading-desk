import os
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

ALPACA_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)


def get_bars(symbol: str):
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        limit=200
    )

    bars = client.get_stock_bars(request)

    df = bars.df

    if df.empty:
        return pd.DataFrame()

    df = df.reset_index()

    # Normalize column names
    df.columns = [col.lower() for col in df.columns]

    return df

