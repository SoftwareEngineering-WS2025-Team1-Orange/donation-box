import json
from dataclasses import asdict
from datetime import datetime

from bright_ws import Router
from websocket import WebSocketApp

from dclasses import ContainerStatusUpdateRequest, ContainerStatusUpdateResponse

from utils.docker_manager import DockerManager, ContainerStatus

status_router = Router()

manager = DockerManager()

@status_router.route(event="containerStatusUpdate")
def status_request(message: dict, ws: WebSocketApp) -> str:
    parsed_data=ContainerStatusUpdateRequest(**message)
    response=ContainerStatusUpdateResponse(time=datetime.now().isoformat(),
                                           runningContainers=[],
                                           abortedContainers=[],
                                           finishedContainers=[],
                                           notFoundContainers=[])
    for containerName in parsed_data.containerNames:
        if manager.get_container_status(containerName) == ContainerStatus.RUNNING:
            response.runningContainers.append(containerName)
        elif manager.get_container_status(containerName) == ContainerStatus.CRASHED:
            response.abortedContainers.append(containerName)
        elif manager.get_container_status(containerName) == ContainerStatus.FINISHED:
            response.finishedContainers.append(containerName)
        else:
            response.notFoundContainers.append(containerName)
    ws.send(json.dumps(asdict(response)))