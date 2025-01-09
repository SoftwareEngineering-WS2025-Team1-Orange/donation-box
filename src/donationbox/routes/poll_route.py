import json
import time

import requests
import threading

from websocket import WebSocketApp
from bright_ws import Router
from dclasses import AddConfigurationRequest, AddConfigurationResponse

from utils import docker_manager
from utils import settings

from donationbox.dclasses import StartMiningRequest

config_router = Router()

@poll_router.route(event="addConfiguration")
def status_request(message: AddConfigurationRequest, ws: WebSocketApp) -> AddConfigurationResponse:
    """
    Handles configuration loading and status checking in a separate thread.

    :param message: AddConfigurationRequest message containing details for setup.
    :param ws: WebSocketApp instance.
    """
    def thread_logic():
        host_port = docker_manager.start_container(StartMiningRequest(imageName=message.image_name,
                                               containerName="pluginContainer",
                                               environmentVars={"api_passkey": settings.passkey}),
                                               isPluginContainer=True)

        health_url = f"http://localhost:{host_port}/health"
        timeout = 60
        interval = 5

        wait_for_ok(health_url, timeout, interval)

        load_config_url = f"http://localhost:{host_port}/load_config"
        poll_url = f"http://localhost:{host_port}/poll"

        try:
            payload = {
                "passkey": settings.passkey,
                "config": message.plugin_configuration
            }

            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(load_config_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 201:
                print("Success:", response.status_code)
            else:
                print("Failed with status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)


    threading.Thread(target=thread_logic).start()