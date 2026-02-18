# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from institutional_engine import latest_signal, latest_prices
from live_ws import start_stream
import threading

app = FastAPI()
templates = Jinja2Templates(directory="templates")

stream_started = False


@app.on_event("startup")
def startup_event():
    global stream_started
    if not stream_started:
        threading.Thread(target=start_stream, daemon=True).start()
        stream_started = True
        print("🚀 Alpaca stream started")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/signals")
def get_signals():
    return latest_signal


@app.get("/prices")
def get_prices():
    return latest_prices

