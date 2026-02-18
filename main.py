from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from institutional_engine import latest_signal
from live_ws import start_stream
import threading

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Start Alpaca stream in background
def run_stream():
    start_stream()

threading.Thread(target=run_stream, daemon=True).start()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/signals")
def get_signals():
    return latest_signal

