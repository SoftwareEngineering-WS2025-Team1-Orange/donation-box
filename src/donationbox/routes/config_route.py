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

def wait_for_ok(endpoint: str, timeout: int = 60, interval: int = 5):
    """
    Synchronously waits for an endpoint to return "OK".

    :param endpoint: The URL of the endpoint to check.
    :param timeout: Total time to wait before timing out (in seconds).
    :param interval: Time between checks (in seconds).
    :return: True if "OK" is returned within the timeout period, otherwise False.
    """
    start_time = time.time()
    while True:
        try:
            response = requests.get(endpoint, headers={"accept": "application/json"})
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get("status", "").lower() == "ok":
                    print("Endpoint returned OK")
                    return True
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print("Timeout reached without receiving OK")
            return False

        time.sleep(interval)

@config_router.route(event="addConfiguration")
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