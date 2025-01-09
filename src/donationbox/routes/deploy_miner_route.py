import json
from dataclasses import asdict

from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartContainerRequest, StartContainerResponse, StopContainerRequest, StopContainerResponse, \
    StopContainerResponseEnum, StartContainerResponseEnum, ContainerStatusEnum

from utils import docker_manager

deploy_router = Router()


@deploy_router.route(event="startMiningRequest")
def startMining(message: StartContainerRequest, ws: WebSocketApp):
    # print(f"Starting container {parsed_data.containerName}")
    if docker_manager.get_container_status(message.containerName) == ContainerStatusEnum.RUNNING:
        # print(f"Starting container {parsed_data.containerName}: ERR_CONTAINER_ALREADY_RUNNING")
        return StartContainerResponse(success=False, response=StartContainerResponseEnum.ERR_CONTAINER_ALREADY_RUNNING)

    success = docker_manager.start_container(message)
    if not success:
        # print(f"Starting container {parsed_data.containerName}: ERR_COULD_NOT_START_CONTAINER")
        return StartContainerResponse(success=False, response=StartContainerResponseEnum.ERR_COULD_NOT_START_CONTAINER)
    # print(f"Starting container {parsed_data.containerName}: success")
    return StartContainerResponse(success=True, response=StartContainerResponseEnum.STARTED_MINING)


@deploy_router.route(event="stopMiningRequest")
def stopMining(message: StopContainerRequest, ws: WebSocketApp):
    if docker_manager.get_container_status(message.containerName) != ContainerStatusEnum.RUNNING:
        ws.send(json.dumps(asdict(StopContainerResponse(status=False,
                                                     response=StopContainerResponseEnum.ERR_CONTAINER_NOT_RUNNING))))
        return
    success = docker_manager.stop_container(message)
    if not success:
        return StopContainerResponse(status=False, response=StopContainerResponseEnum.ERR_OTHER)
    return StopContainerResponse(status=True, response=StopContainerResponseEnum.STOPPED_MINING)
