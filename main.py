from fastapi import FastAPI
from market_data import get_bars
from indicators import calculate_indicators
from regime import calculate_regime
from risk_engine import calculate_position_size

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Trading Desk Engine Running"}


@app.get("/scanner")
def scanner():

    symbols = ["TSLA", "NVDA", "MSFT", "AAPL", "GOOGL", "XOM"]

    results = []

    for symbol in symbols:

        df = get_bars(symbol)

        if df.empty:
            continue

        df = calculate_indicators(df)

        regime_score = calculate_regime(df)

        latest = df.iloc[-1]

        regime = (
            "Trend" if regime_score >= 70 else
            "Range" if regime_score < 40 else
            "Neutral"
        )

        results.append({
            "symbol": symbol,
            "price": round(latest["close"], 2),
            "rvol": round(latest["rvol"], 2),
            "regime_score": regime_score,
            "regime": regime
        })

    return results


@app.get("/risk")
def risk(
    account_size: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float
):

    stop_distance = abs(entry_price - stop_price)

    shares = calculate_position_size(
        account_size,
        risk_percent,
        stop_distance
    )

    return {
        "shares": round(shares, 2),
        "risk_per_share": round(stop_distance, 2),
        "2R_target": round(entry_price + 2 * stop_distance, 2)
    }

