import json
import threading
import time

from websocket import WebSocketApp

from bright_ws import Lifecycle
from utils.settings import settings
import random
from routes.status_route import status_update

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

    def periodic_status_update():
        while True:
            try:
                time.sleep(random.randint(110, 130))
                status_update({}, ws)
            except Exception:
                break

    thread = threading.Thread(target=periodic_status_update)
    thread.daemon = True

    thread.start()
