import json
import subprocess
from websocket import WebSocketApp

from ..annotations.routes import route
from ..dclasses import StartMiningRequest, StartMiningResponse, StopMiningRequest, StopMiningResponse, \
    StopMiningResponseEnum, StartMiningResponseEnum


running_containers = []

@route(event="startMiningCommand")
def startMining(ws: WebSocketApp, message: dict) -> str:
    parsed_request = StartMiningRequest(**message)
    env_vars = " ".join([f"-e {key}={value}" for key, value in parsed_request.environmentVars.items()])
    subprocess.run(f"docker run -itd --restart=always {env_vars} "
                   f"--name {parsed_request.containerName} {parsed_request.imageName}", shell=True)
    running_containers.append(parsed_request.containerName)
    ws.send(json.dumps(StartMiningResponse(success=True, response = StartMiningResponseEnum.STARTED_MINING)))
    pass


@route(event="stopMiningCommand")
def stopMining(ws: WebSocketApp, message: dict) -> str:
    parsed_request = StopMiningRequest(**message)
    subprocess.run(f"docker stop {parsed_request.containerName}", shell=True)
    subprocess.run(f"docker rm {parsed_request.containerName}", shell=True)
    running_containers.remove(parsed_request.containerName)
    ws.send(json.dumps(StopMiningResponse(status=True,response = StopMiningResponseEnum.STOPPED_MINING)))
    pass
