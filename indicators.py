import pandas as pd
import ta

def calculate_indicators(df):
    df['ema20'] = ta.trend.ema_indicator(df['close'], window=20)
    df['ema50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    # Relative Volume
    df['volume_avg'] = df['volume'].rolling(20).mean()
    df['rvol'] = df['volume'] / df['volume_avg']

    # VWAP
    df['cum_volume'] = df['volume'].cumsum()
    df['cum_volume_price'] = (df['close'] * df['volume']).cumsum()
    df['vwap'] = df['cum_volume_price'] / df['cum_volume']
    df['vwap_distance'] = df['close'] - df['vwap']

    # Liquidity Sweep Detection
    df['prev_5_low'] = df['low'].rolling(5).min().shift(1)
    df['prev_5_high'] = df['high'].rolling(5).max().shift(1)

    df['bullish_sweep'] = (
        (df['low'] < df['prev_5_low']) &
        (df['close'] > df['prev_5_low']) &
        (df['rvol'] > 1.2)
    )

    df['bearish_sweep'] = (
        (df['high'] > df['prev_5_high']) &
        (df['close'] < df['prev_5_high']) &
        (df['rvol'] > 1.2)
    )

    # Identify swing lows
   df['swing_low'] = (
        (df['low'] < df['low'].shift(1)) &
        (df['low'] < df['low'].shift(2)) &
        (df['low'] < df['low'].shift(-1)) &
        (df['low'] < df['low'].shift(-2))
    )

   # Identify swing highs
   df['swing_high'] = (
        (df['high'] > df['high'].shift(1)) &
        (df['high'] > df['high'].shift(2)) &
        (df['high'] > df['high'].shift(-1)) &
        (df['high'] > df['high'].shift(-2))
    )
    return df
