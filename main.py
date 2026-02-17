from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from market_data import get_bars
from indicators import calculate_indicators
from regime import classify_regime
from risk_engine import calculate_position

from database import init_db, SessionLocal, Watchlist

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize database
init_db()

# Seed initial watchlist if empty
db_seed = SessionLocal()
if db_seed.query(Watchlist).count() == 0:
    for sym in ["TSLA", "NVDA", "MSFT", "AAPL", "GOOGL", "XOM"]:
        db_seed.add(Watchlist(symbol=sym))
    db_seed.commit()
db_seed.close()


@app.get("/")
def home():
    return {"message": "Trading Desk Engine Running"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


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


@app.get("/scanner")
def scanner():
    db = SessionLocal()
    watchlist = db.query(Watchlist).all()
    symbols = [w.symbol for w in watchlist]

    results = []

for symbol in symbols:
    try:
        df = get_bars(symbol)

        if df is None or df.empty or 'close' not in df.columns:
            continue

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

    except Exception as e:
        print(f"Skipping {symbol}: {e}")
        continue

    db.close()

    results = sorted(results, key=lambda x: x['trade_bias_score'], reverse=True)

    return results


@app.post("/add_symbol/{symbol}")
def add_symbol(symbol: str):
    db = SessionLocal()
    symbol = symbol.upper()

    existing = db.query(Watchlist).filter(Watchlist.symbol == symbol).first()
    if existing:
        db.close()
        return {"message": "Symbol already exists"}

    new_symbol = Watchlist(symbol=symbol)
    db.add(new_symbol)
    db.commit()
    db.close()

    return {"message": f"{symbol} added"}


@app.delete("/remove_symbol/{symbol}")
def remove_symbol(symbol: str):
    db = SessionLocal()
    symbol = symbol.upper()

    item = db.query(Watchlist).filter(Watchlist.symbol == symbol).first()
    if not item:
        db.close()
        return {"message": "Symbol not found"}

    db.delete(item)
    db.commit()
    db.close()

    return {"message": f"{symbol} removed"}


@app.get("/risk")
def risk(entry: float, stop: float):
    return calculate_position(entry, stop)

