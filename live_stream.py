import asyncio
import websockets
import json

ALPACA_KEY = "PKEM365TC6FHNKHBXBPME3QKNQ"
ALPACA_SECRET = "H7YMAgivDk3QrPZuGAge7oW67JECPhgaYtApzJ662mhT"

SYMBOLS = ["TSLA", "NVDA", "SPY"]

async def stream():
    uri = "wss://stream.data.alpaca.markets/v2/iex"

    async with websockets.connect(uri) as ws:

        # Wait for connected message
        connected_msg = await ws.recv()
        print("Connected:", connected_msg)

        # Authenticate
        await ws.send(json.dumps({
            "action": "auth",
            "key": ALPACA_KEY,
            "secret": ALPACA_SECRET
        }))

        auth_msg = await ws.recv()
        print("Auth:", auth_msg)

        if "authenticated" not in auth_msg:
            print("Authentication failed.")
            return

        # Subscribe to minute bars
        await ws.send(json.dumps({
            "action": "subscribe",
            "bars": SYMBOLS
        }))

        sub_msg = await ws.recv()
        print("Subscribed:", sub_msg)

        # Listen for live bars
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            for event in data:
                if event.get("T") == "b":
                    print(f"\nLIVE BAR {event['S']}")
                    print("Open:", event["o"])
                    print("High:", event["h"])
                    print("Low:", event["l"])
                    print("Close:", event["c"])
                    print("Volume:", event["v"])

asyncio.run(stream())
