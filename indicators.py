import ta


def calculate_indicators(df):

    # EMAs
    df['ema20'] = ta.trend.ema_indicator(df['close'], window=20)
    df['ema50'] = ta.trend.ema_indicator(df['close'], window=50)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    # VWAP
    df['vwap'] = ta.volume.volume_weighted_average_price(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        volume=df['volume']
    )

    df['vwap_distance'] = df['close'] - df['vwap']

    # Relative Volume
    df['rvol'] = df['volume'] / df['volume'].rolling(20).mean()

    # Liquidity Sweeps
    df['bullish_sweep'] = df['low'] < df['low'].shift(1)
    df['bearish_sweep'] = df['high'] > df['high'].shift(1)

    # Swing Low (5-min structure)
    df['swing_low'] = (
        (df['low'] < df['low'].shift(1)) &
        (df['low'] < df['low'].shift(2)) &
        (df['low'] < df['low'].shift(-1)) &
        (df['low'] < df['low'].shift(-2))
    )

    # Swing High (5-min structure)
    df['swing_high'] = (
        (df['high'] > df['high'].shift(1)) &
        (df['high'] > df['high'].shift(2)) &
        (df['high'] > df['high'].shift(-1)) &
        (df['high'] > df['high'].shift(-2))
    )

    return df

