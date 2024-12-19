from bright_ws import Router
from websocket import WebSocketApp

auth_router = Router()


@auth_router.route(event="authResponse")
def authenticate_response(message: dict, ws: WebSocketApp):
    pass
