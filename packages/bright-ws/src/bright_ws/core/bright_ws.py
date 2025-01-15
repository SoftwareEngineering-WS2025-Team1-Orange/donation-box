import json
from typing import Any, Callable

import websocket
import rel

from ..config.config import BrightConfig
from ..dclasses import Event
from websocket import WebSocketApp

import inspect


def dispatch_event(routes: dict[str: Callable]):
    def wrapper(ws: WebSocketApp, message: Any):
        to_object = Event.from_dict(json.loads(message))
        func = routes[to_object.event]
        number = len(inspect.signature(func).parameters.keys())
        if number == 1:
            routes[to_object.event](to_object.data)
        else:
            routes[to_object.event](to_object.data, ws)

    return wrapper


def collect_routes(config: BrightConfig):
    routes = {}
    for router in config.routes:
        for key in router._store.keys():
            routes[key] = router._store[key]
    return routes


def collect_lifecycle(config: BrightConfig):
    lifecycle = {}
    for life in config.lifecycle:
        for key in life._store.keys():
            lifecycle[key] = life._store[key]
    return lifecycle


class BrightWs:
    def __init__(self, config: BrightConfig):
        self.config = config

    def start(self):
        routes = collect_routes(self.config)
        lifecycles = collect_lifecycle(self.config)

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(self.config.host_url,
                                    on_open=lifecycles["on_open"],
                                    on_message=dispatch_event(routes),
                                    on_error=lifecycles["on_error"],
                                    on_close=lifecycles["on_close"])

        ws.run_forever(dispatcher=rel,
                       reconnect=5)
        rel.signal(2, rel.abort)
        rel.dispatch()
