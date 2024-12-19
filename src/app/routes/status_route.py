import json
from ..annotations.routes import route
from ..utils.settings import settings
from websocket import WebSocketApp
from .deploy_miner_route import running_containers


@route(event="statusRequest")
def status_request(ws: WebSocketApp, message: dict) -> str:

    pass
