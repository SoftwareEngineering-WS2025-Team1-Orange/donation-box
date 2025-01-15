import json
import sys
from dataclasses import asdict

from bright_ws import Router
from websocket import WebSocketApp
from dclasses import AuthResponse, ContainerStatusMessageEnum, ContainerStatusCodeEnum
from utils import docker_manager
from routes.status_route import get_status

auth_router = Router()


@auth_router.route(event="authResponse")
def authenticate_response(message: AuthResponse, ws: WebSocketApp):
    if not message.success:
        print("Error: Could not authenticate to mainframe", file=sys.stderr)
        exit(1)
    for container_name in message.monitored_containers:
        if docker_manager.exists(container_name):
            status = docker_manager.get_container_status(container_name).statusMsg
            if status == ContainerStatusMessageEnum.CRASHED or status == ContainerStatusMessageEnum.FINISHED:
                docker_manager.remove_container(container_name)
            else:
                docker_manager.add_monitored_container(container_name)

    status = get_status()
    for container in status.container:
        if container.containerName == 'pluginContainer':
            container.statusCode = ContainerStatusCodeEnum.ERROR if status.power_supply is None \
                else ContainerStatusCodeEnum.OK
            container.statusMsg = ContainerStatusMessageEnum.ERROR if status.power_supply is None \
                else ContainerStatusMessageEnum.OK
    ws.send(json.dumps({'event': 'statusUpdateResponse', 'data': asdict(status)}))
    return None
