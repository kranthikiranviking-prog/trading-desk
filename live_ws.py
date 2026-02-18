import asyncio
import json
import websockets
from fastapi import WebSocket
import os

ALPACA_KEY = "YOUR_KEY"
ALPACA_SECRET = "YOUR_SECRET"

ALPACA_WS = "wss://stream.data.alpaca.markets/v2/iex"

symbols = ["TSLA", "NVDA", "SPY"]

connected_clients = set()

async def alpaca_stream():
    async with websockets.connect(ALPACA_WS) as ws:

        # Authenticate
        await ws.send(json.dumps({
            "action": "auth",
            "key": ALPACA_KEY,
            "secret": ALPACA_SECRET
        }))

        await ws.recv()

        # Subscribe to minute bars
        await ws.send(json.dumps({
            "action": "subscribe",
            "bars": symbols
        }))

        await ws.recv()

        while True:
            message = await ws.recv()
            data = json.loads(message)

            for client in connected_clients:
                await client.send_text(message)


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)

