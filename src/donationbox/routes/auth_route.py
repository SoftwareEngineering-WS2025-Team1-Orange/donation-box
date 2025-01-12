import sys
from bright_ws import Router
from websocket import WebSocketApp
from dclasses import AuthResponse, ContainerStatusEnum
from utils import docker_manager

auth_router = Router()


@auth_router.route(event="authResponse")
def authenticate_response(message: AuthResponse, ws: WebSocketApp):
    if not message.success:
        print("Error: Could not authenticate to mainframe", file=sys.stderr)
        exit(1)
    for container_name in message.monitored_containers:
        if docker_manager.exists(container_name):
            status = docker_manager.get_container_status(container_name)
            if status == ContainerStatusEnum.CRASHED or status == ContainerStatusEnum.FINISHED:
                docker_manager.remove_container(container_name)
            else:
                docker_manager.add_monitored_container(container_name)
    return None
