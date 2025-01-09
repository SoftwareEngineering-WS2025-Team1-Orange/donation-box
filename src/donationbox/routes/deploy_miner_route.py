import json
from dataclasses import asdict

from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartMiningRequest, StartMiningResponse, StopMiningRequest, StopMiningResponse, \
    StopMiningResponseEnum, StartMiningResponseEnum, ContainerStatusEnum

from utils import docker_manager

deploy_router = Router()


@deploy_router.route(event="startMiningRequest")
def startMining(message: StartMiningRequest, ws: WebSocketApp):
    # print(f"Starting container {parsed_data.containerName}")
    if docker_manager.get_container_status(message.containerName) == ContainerStatusEnum.RUNNING:
        # print(f"Starting container {parsed_data.containerName}: ERR_CONTAINER_ALREADY_RUNNING")
        return StartMiningResponse(success=False, response=StartMiningResponseEnum.ERR_CONTAINER_ALREADY_RUNNING)

    success = docker_manager.start_container(message)
    if not success:
        # print(f"Starting container {parsed_data.containerName}: ERR_COULD_NOT_START_CONTAINER")
        ws.send(json.dumps(asdict(StartMiningResponse(success=False,
                                                      response=StartMiningResponseEnum.ERR_COULD_NOT_START_CONTAINER))))
        return
    # print(f"Starting container {parsed_data.containerName}: success")
    return StartMiningResponse(success=True, response=StartMiningResponseEnum.STARTED_MINING)


@deploy_router.route(event="stopMiningRequest")
def stopMining(message: StopMiningRequest, ws: WebSocketApp):
    if docker_manager.get_container_status(message.containerName) != ContainerStatusEnum.RUNNING:
        ws.send(json.dumps(asdict(StopMiningResponse(status=False,
                                                     response=StopMiningResponseEnum.ERR_CONTAINER_NOT_RUNNING))))
        return
    success = docker_manager.stop_container(message)
    if not success:
        ws.send(json.dumps(asdict(StopMiningResponse(status=False, response=StopMiningResponseEnum.ERR_OTHER))))
        return
    ws.send(json.dumps(asdict(StopMiningResponse(status=True, response=StopMiningResponseEnum.STOPPED_MINING))))
