import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

def get_bars(symbol: str, timeframe=TimeFrame.Minute, limit=100):
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=datetime.now() - timedelta(days=5)
    )
    bars = client.get_stock_bars(request).df
    df = bars.reset_index()
    return df.tail(limit)
