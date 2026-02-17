from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from market_data import get_data
from indicators import calculate_indicators
from regime import calculate_regime
from risk_engine import calculate_position_size

from database import SessionLocal, Watchlist

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ===============================
# DATABASE HELPER
# ===============================

def get_watchlist():
    db: Session = SessionLocal()
    symbols = db.query(Watchlist).all()
    db.close()
    return [s.symbol for s in symbols]


# ===============================
# MARKET CONTEXT
# ===============================

def get_market_context():
    symbols = ["SPY", "QQQ", "VIXY"]
    context = {}

    for symbol in symbols:
        try:
            df = get_data(symbol)
            df = calculate_indicators(df)
            regime_score = calculate_regime(df)

            price = df["close"].iloc[-1]

            regime = (
                "Trend" if regime_score > 70 else
                "Range" if regime_score < 40 else
                "Neutral"
            )

            context[symbol] = {
                "price": round(price, 2),
                "regime": regime
            }

        except Exception:
            context[symbol] = {
                "price": None,
                "regime": "Error"
            }

    # Market Bias Logic
    if (
        context["SPY"]["regime"] == "Trend" and
        context["QQQ"]["regime"] == "Trend"
    ):
        bias = "Risk-On"
    elif context["SPY"]["regime"] == "Range":
        bias = "Choppy"
    else:
        bias = "Mixed"

    context["market_bias"] = bias

    return context


# ===============================
# ROOT
# ===============================

@app.get("/")
def home():
    return {"message": "Trading Desk Engine Running"}


# ===============================
# SCANNER
# ===============================

@app.get("/scanner")
def scanner():
    results = []

    symbols = get_watchlist()

    for symbol in symbols:
        try:
            df = get_data(symbol)
            df = calculate_indicators(df)

            regime_score = calculate_regime(df)

            price = df["close"].iloc[-1]
            rvol = df["volume"].iloc[-1] / df["volume"].rolling(20).mean().iloc[-1]

            regime = (
                "Trend" if regime_score > 70 else
                "Range" if regime_score < 40 else
                "Neutral"
            )

            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "rvol": round(rvol, 2),
                "regime": regime,
                "trade_bias_score": regime_score
            })

        except Exception:
            continue

    return results


# ===============================
# RISK CALCULATOR
# ===============================

@app.get("/risk")
def risk(symbol: str, account_size: float, risk_percent: float, stop_distance: float):

    position_size = calculate_position_size(
        account_size=account_size,
        risk_percent=risk_percent,
        stop_distance=stop_distance
    )

    return {
        "symbol": symbol,
        "shares": round(position_size, 2)
    }


# ===============================
# DASHBOARD
# ===============================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    market_context = get_market_context()
    symbols = get_watchlist()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "market_context": market_context,
            "symbols": symbols
        }
    )

