import json

from websocket import WebSocketApp

from bright_ws import Lifecycle
from utils.settings import settings

lifecycle = Lifecycle()


@lifecycle.exceptionhandler(exception=Exception)
def on_error(ws, error):
    print(f"Error: {error}")


@lifecycle.on_close()
def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


@lifecycle.on_open()
def on_open(ws: WebSocketApp):
    dict = {
        "event": "authRequest",
        "data": {
            "token": settings.jwt}
    }
    ws.send(json.dumps(dict))
