from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartContainerRequest, StartContainerResponse, StopContainerRequest, StopContainerResponse, \
    StopContainerResponseEnum, StartContainerResponseEnum, AddErrorResponse

from utils import docker_manager

deploy_router = Router()


@deploy_router.route(event="startContainerRequest")
def start_container(message: StartContainerRequest, ws: WebSocketApp):
    match docker_manager.start_container(message):
        case docker_manager.StartContainerResult.ALREADY_RUNNING:
            return AddErrorResponse(containerName=message.containerName,
                                    statusCode=4,
                                    statusMsg=StartContainerResponseEnum.ERR_CONTAINER_ALREADY_RUNNING)
        case docker_manager.StartContainerResult.IMAGE_NOT_FOUND:
            return AddErrorResponse(containerName=message.containerName,
                                    statusCode=5,
                                    statusMsg=StartContainerResponseEnum.ERR_IMAGE_NOT_FOUND)
        case docker_manager.StartContainerResult.ERROR:
            return AddErrorResponse(containerName=message.containerName,
                                    statusCode=6,
                                    statusMsg=StartContainerResponseEnum.ERR_COULD_NOT_START_CONTAINER)
        case _:
            return StartContainerResponse(success=True, response=StartContainerResponseEnum.STARTED_CONTAINER)


@deploy_router.route(event="stopContainerRequest")
def stop_container(message: StopContainerRequest, ws: WebSocketApp):
    match docker_manager.remove_container(message.containerName):
        case docker_manager.StopRemoveContainerResult.CONTAINER_NOT_FOUND:
            return StopContainerResponse(status=False, response=StopContainerResponseEnum.ERR_CONTAINER_NOT_RUNNING)
        case docker_manager.StopRemoveContainerResult.ERROR:
            return StopContainerResponse(status=False, response=StopContainerResponseEnum.ERR_OTHER)
        case _:
            return StopContainerResponse(status=True, response=StopContainerResponseEnum.STOPPED_CONTAINER)
