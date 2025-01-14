import json
import threading
import time
from dataclasses import asdict

from websocket import WebSocketApp

from bright_ws import Lifecycle
from utils.settings import settings
import random
from routes.status_route import status_update, get_status

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

    status = get_status()
    for container in status.container:
        if container.containerName == 'pluginContainer':
            container.statusCode = 1 if status.power_supply is None else 0
            container.statusMsg = "Error" if status.power_supply is None else "Ok"
    ws.send(json.dumps(asdict(status)))



    def print_message():
        while True:
            time.sleep(random.randint(110, 130))
            status_update({}, ws)

    thread = threading.Thread(target=print_message)
    thread.daemon = True

    thread.start()
