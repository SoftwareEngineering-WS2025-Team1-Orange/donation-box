import websocket
import rel

from ..routes.route_handler import dispatch_event
from ..utils import settings
from ..routes.auth_route import authenticate_request



def event_loop():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(settings.mainframe_socket_url,
                                on_open=authenticate_request,
                                on_message=dispatch_event,
                                on_error=lambda ws, error: rel.signal(2, error),
                                on_close=lambda ws: rel.signal(3, "Closed connection"))

    ws.run_forever(dispatcher=rel,
                   reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()
