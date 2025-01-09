import json
from dataclasses import asdict

from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartMiningRequest, StartMiningResponse, StopMiningRequest, StopMiningResponse, \
    StopMiningResponseEnum, StartMiningResponseEnum

from utils.docker_manager import DockerManager, ContainerStatus

deploy_router = Router()
manager = DockerManager()



@deploy_router.route(event="startMiningRequest")
def startMining(message: dict, ws: WebSocketApp):
    parsed_data = StartMiningRequest(**message)
    if manager.get_container_status(parsed_data.containerName) == ContainerStatus.RUNNING:
        ws.send(json.dumps(asdict(StartMiningResponse(success=False,
                                                      response=StartMiningResponseEnum.ERR_CONTAINER_ALREADY_RUNNING))))
        return

    success = manager.start_container(parsed_data)
    if not success:
        ws.send(json.dumps(asdict(StartMiningResponse(success=False,
                                                      response=StartMiningResponseEnum.ERR_COULD_NOT_START_CONTAINER))))
        return
    ws.send(json.dumps(asdict(StartMiningResponse(success=True, response=StartMiningResponseEnum.STARTED_MINING))))


@deploy_router.route(event="stopMiningRequest")
def stopMining(message: StopMiningRequest, ws: WebSocketApp):
    parsed_data = StopMiningRequest(**message)
    if manager.get_container_status(parsed_data.containerName) != ContainerStatus.RUNNING:
        ws.send(json.dumps(asdict(StopMiningResponse(status=False,
                                                     response=StopMiningResponseEnum.ERR_CONTAINER_NOT_RUNNING))))
        return
    success = manager.stop_container(parsed_data)
    if not success:
        ws.send(json.dumps(asdict(StopMiningResponse(status=False, response=StopMiningResponseEnum.ERR_OTHER))))
        return
    ws.send(json.dumps(asdict(StopMiningResponse(status=True, response=StopMiningResponseEnum.STOPPED_MINING))))




