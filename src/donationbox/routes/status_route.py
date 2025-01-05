from bright_ws import Router
from websocket import WebSocketApp

status_router = Router()


@status_router.route(event="statusRequest")
def status_request(message: dict, ws: WebSocketApp) -> str:
    pass
