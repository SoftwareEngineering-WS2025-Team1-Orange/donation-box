from websocket import WebSocketApp

from ..annotations.routes import dispatcher
from ..dclasses import Event
from ..utils.route_store import route_store


@dispatcher
def dispatch_event(ws: WebSocketApp, message: Event):
    route_store.get_route(message.event)(message.data)

