import json
from ..annotations.routes import route
from ..utils.settings import settings
from websocket import WebSocketApp


def authenticate_request(ws: WebSocketApp):
    request = {
        "event": "authRequest",
        "data": {
            "token": settings.jwt}
    }
    ws.send(json.dumps(request))


@route(event="authResponse")
def authenticate_response(ws: WebSocketApp, message: dict) -> str:
    pass
