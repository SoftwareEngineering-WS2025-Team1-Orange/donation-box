import json
import os
import time
import socket
from dataclasses import asdict

import requests
import threading

from websocket import WebSocketApp
from bright_ws import Router
from dclasses import AddConfigurationRequest, AddConfigurationResponse, StoredConfiguration, ContainerStatus

from utils import docker_manager
from utils import settings
from utils.encryption import store_json_encrypted

from routes.status_route import get_status
from donationbox.dclasses import StartContainerRequest

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
            print(f"Error connecting to plugin: {e}")

        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print("Timeout reached without receiving OK")
            return False

        time.sleep(interval)


def find_free_port(start_port=50000):
    for port in range(start_port, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError("Could not find a free port")


@config_router.route(event="addConfigurationRequest")
def add_configuration_request(message: AddConfigurationRequest, ws: WebSocketApp) -> AddConfigurationResponse:
    """
    Handles configuration loading and status checking in a separate thread.

    :param message: AddConfigurationRequest message containing details for setup.
    :param ws: WebSocketApp instance.
    """

    def thread_logic(ws: WebSocketApp):
        port = find_free_port()
        match docker_manager.start_container(StartContainerRequest(imageName=message.plugin_image_name,
                                                                   containerName="pluginContainer",
                                                                   environmentVars={"api_passkey": settings.passkey}),
                                             port={'int': '8000/tcp', 'ext': port}):
            case docker_manager.StartContainerResult.SUCCESS:
                pass
            case docker_manager.StartContainerResult.ALREADY_RUNNING:
                port = docker_manager.get_container_port("pluginContainer")
            case _:
                print("Failed to start container")

        health_url = f"http://localhost:{port}/health"
        timeout = 60
        interval = 5

        assert wait_for_ok(health_url, timeout, interval), "Plugin health did not return OK within timeout period"

        load_config_url = f"http://localhost:{port}/load_config"

        try:
            payload = {
                "passkey": settings.passkey,
                "config": message.plugin_configuration
            }

            headers = {
                "Content-Type": "application/json"
            }

            requests.post(load_config_url, data=json.dumps(payload), headers=headers)

            status = get_status()

            for container in status.container:
                if container.containerName == 'pluginContainer':
                    container.statusCode = 1 if status.power_supply is None else 0
                    container.statusMsg = "Error" if status.power_supply is None else "Ok"

            ws.send(json.dumps(asdict(status)))

            if status.power_supply is not None:
                print("Load config: Success")
                store_json_encrypted(asdict(
                    StoredConfiguration(image_name=message.plugin_image_name,
                                        port={'int': '8000/tcp', 'ext': port},
                                        plugin_configuration=message.plugin_configuration)), 'config.json')

        except requests.exceptions.RequestException as e:
            print("An error occurred loading config data:", e)

    status = get_status()
    for container in status.container:
        if container.containerName == 'pluginContainer':
            status.container.remove(container)
    status.container.append(
        ContainerStatus(
            containerName='pluginContainer',
            statusCode='100',
            statusMsg='Pending'
        )
    )
    ws.send(json.dumps(asdict(status)))
    try:
        os.remove("config.json")
    except FileNotFoundError:
        pass
    threading.Thread(target=thread_logic(ws=ws)).start()
