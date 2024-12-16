import json
import functools
from typing import Callable
from ..dclasses import Event
from websocket import WebSocketApp
from ..utils.route_store import route_store


def dispatcher(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(ws: WebSocketApp, message: str, **kwargs):
        return func(ws, Event.from_dict(json.loads(message)), **kwargs)

    return wrapper


def route(event: str):
    def decorator(func):
        print(f"Adding route for {event}")
        route_store.add_route(event, func)
