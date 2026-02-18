# main.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from institutional_engine import latest_signal
from live_ws import start_stream
import threading

app = FastAPI()

# Start Alpaca stream in background thread
def run_stream():
    start_stream()

threading.Thread(target=run_stream, daemon=True).start()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("dashboard.html", "r") as f:
        return f.read()


@app.get("/signals")
def get_signals():
    return latest_signal

