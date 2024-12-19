import json
import subprocess
from bright_ws import Router
from websocket import WebSocketApp
from dclasses import StartMiningRequest, StartMiningResponse, StopMiningRequest, StopMiningResponse, \
    StopMiningResponseEnum, StartMiningResponseEnum

deploy_router = Router()

running_containers = []


@deploy_router.route(event="startMiningCommand")
def startMining(message: StartMiningRequest, ws: WebSocketApp):
    env_vars = " ".join([f"-e {key}={value}" for key, value in message.environmentVars.items()])
    subprocess.run(f"docker run -itd --restart=always {env_vars} "
                   f"--name {message.containerName} {message.imageName}", shell=True)
    running_containers.append(message.containerName)
    ws.send(json.dumps(StartMiningResponse(success=True, response=StartMiningResponseEnum.STARTED_MINING)))


@deploy_router.route(event="stopMiningCommand")
def stopMining(message: StopMiningRequest, ws: WebSocketApp):
    subprocess.run(f"docker stop {message.containerName}", shell=True)
    subprocess.run(f"docker rm {message.containerName}", shell=True)
    running_containers.remove(message.containerName)
    ws.send(json.dumps(StopMiningResponse(status=True, response=StopMiningResponseEnum.STOPPED_MINING)))
