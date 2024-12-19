import websocket
import rel

from ..routes.route_handler import dispatch_event
from ..utils import settings
from ..routes.auth_route import authenticate_request

import importlib
import pkgutil


def event_loop():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(settings.mainframe_socket_url,
                                on_open=on_open,
                                on_message=dispatch_event,
                                on_error=on_error,
                                on_close=lambda ws: rel.signal(3, "Closed connection"))

    ws.run_forever(dispatcher=rel,
                   reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()

def on_error(ws, error):
    print(f"Error: {error}")

def on_open(ws: websocket.WebSocketApp):
    print("Connection opened")
    package_path = "src/app/routes"
    load_modules_from_package(package_path)
    authenticate_request(ws)

def load_modules_from_package(package_name):
    # Iterate over all modules in the package
    for _, module_name, is_pkg in pkgutil.iter_modules([package_name]):
        if not is_pkg:  # Ignore subpackages
            try:
                importlib.import_module(f"{package_name}/{module_name}".replace("/", "."))
                print(f"Module '{module_name}' loaded successfully.")
            except Exception as e:
                print(f"Failed to load module '{module_name}': {e}")