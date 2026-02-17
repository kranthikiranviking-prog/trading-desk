from fastapi import FastAPI
from market_data import get_bars
from indicators import calculate_indicators
from regime import classify_regime
from risk_engine import calculate_position
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Trading Desk Engine Running"}

@app.get("/stock/{symbol}")
def analyze_stock(symbol: str):
    df = get_bars(symbol.upper())
    df = calculate_indicators(df)
    score, regime = classify_regime(df)

    latest = df.iloc[-1]

    return {
        "symbol": symbol.upper(),
        "price": round(latest['close'], 2),
        "rvol": round(latest['rvol'], 2),
        "ema20": round(latest['ema20'], 2),
        "ema50": round(latest['ema50'], 2),
        "vwap": round(latest['vwap'], 2),
        "vwap_distance": round(latest['vwap_distance'], 2),
        "rsi": round(latest['rsi'], 2),
        "bullish_sweep": bool(latest['bullish_sweep']),
        "bearish_sweep": bool(latest['bearish_sweep']),
        "regime_score": score,
        "regime": regime
    }

@app.get("/risk")
def risk(entry: float, stop: float):
    return calculate_position(entry, stop)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/scanner")
def scanner():
    watchlist = ["TSLA", "NVDA", "MSFT", "AAPL", "GOOGL", "XOM"]
    results = []

    for symbol in watchlist:
        df = get_bars(symbol)
        df = calculate_indicators(df)
        score, regime = classify_regime(df)
        latest = df.iloc[-1]

        trade_bias = 0

        if regime == "Trend":
            trade_bias += 30
        if latest['rvol'] > 2:
            trade_bias += 20
        if latest['bullish_sweep']:
            trade_bias += 20
        if latest['bearish_sweep']:
            trade_bias -= 20
        if latest['vwap_distance'] > 0:
            trade_bias += 10

        results.append({
            "symbol": symbol,
            "price": round(latest['close'], 2),
            "rvol": round(latest['rvol'], 2),
            "regime": regime,
            "bullish_sweep": bool(latest['bullish_sweep']),
            "bearish_sweep": bool(latest['bearish_sweep']),
            "trade_bias_score": trade_bias
        })

    results = sorted(results, key=lambda x: x['trade_bias_score'], reverse=True)

    return results
