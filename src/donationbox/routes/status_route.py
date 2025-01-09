from datetime import datetime
from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StatusUpdateResponse, SolarStatusUpdateResponse
from utils import docker_manager

status_router = Router()


@status_router.route(event="statusRequest")
def status_update(message: dict, ws: WebSocketApp):
    response = StatusUpdateResponse(time=datetime.now().isoformat(),
                                    solar=SolarStatusUpdateResponse(),
                                    container={})
    for container_name in docker_manager.get_monitored_containers():
        response.container[container_name] = docker_manager.get_container_status(container_name)
    return response
