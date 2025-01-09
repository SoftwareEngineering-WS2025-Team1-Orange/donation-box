from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartContainerRequest, StartContainerResponse, StopContainerRequest, StopContainerResponse, \
    StopContainerResponseEnum, StartContainerResponseEnum, ContainerStatusEnum

from utils import docker_manager

deploy_router = Router()


@deploy_router.route(event="startContainerRequest")
def startContainer(message: StartContainerRequest, ws: WebSocketApp):
    if docker_manager.get_container_status(message.containerName) == ContainerStatusEnum.RUNNING:
        return StartContainerResponse(success=False, response=StartContainerResponseEnum.ERR_CONTAINER_ALREADY_RUNNING)

    success = docker_manager.start_container(message)
    if not success:
        return StartContainerResponse(success=False, response=StartContainerResponseEnum.ERR_COULD_NOT_START_CONTAINER)
    return StartContainerResponse(success=True, response=StartContainerResponseEnum.STARTED_MINING)


@deploy_router.route(event="stopContainerRequest")
def stopContainer(message: StopContainerRequest, ws: WebSocketApp):
    if docker_manager.get_container_status(message.containerName) != ContainerStatusEnum.RUNNING:
        return StopContainerResponse(status=False, response=StopContainerResponseEnum.ERR_CONTAINER_NOT_RUNNING)

    success = docker_manager.stop_container(message)
    if not success:
        return StopContainerResponse(status=False, response=StopContainerResponseEnum.ERR_OTHER)
    return StopContainerResponse(status=True, response=StopContainerResponseEnum.STOPPED_MINING)
