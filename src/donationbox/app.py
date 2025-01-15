import json

from bright_ws.config.config import BrightConfig
from bright_ws.core.bright_ws import BrightWs
from routes.config_route import config_router
from utils import settings
from utils.encryption import load_json_encrypted
from utils import docker_manager

from lifecycle.lifecycle import lifecycle
from routes.auth_route import auth_router
from routes.status_route import status_router
from routes.deploy_miner_route import deploy_router
from dclasses import StoredConfiguration, StartContainerRequest
from routes.config_route import wait_for_ok
import requests

running = False

bright_ws = BrightWs(config=BrightConfig(
    host_url=settings.mainframe_socket_url,
    lifecycle=[lifecycle],
    routes=[auth_router,
            status_router,
            deploy_router,
            config_router,
            ],
))


def main():
    # Load configuration
    try:
        config = StoredConfiguration(**load_json_encrypted('config.json'))
        print("Loaded configuration")
        match docker_manager.start_container(StartContainerRequest(imageName=config.image_name,
                                                                   containerName="pluginContainer",
                                                                   environmentVars={"api_passkey": settings.passkey}),
                                             port=config.port):
            case docker_manager.StartContainerResult.SUCCESS:
                pass
            case docker_manager.StartContainerResult.ALREADY_RUNNING:
                pass
            case _:
                raise Exception("Failed to start plugin container")

        plugin_url = f"http://{settings.api_dns}:{config.port['ext']}"

        assert wait_for_ok(f"{plugin_url}/health", timeout=120,
                           interval=5), "Plugin health did not return OK within timeout period"

        payload = {
            "passkey": settings.passkey,
            "config": config.plugin_configuration
        }

        headers = {
            "Content-Type": "application/json"
        }

        requests.post(url=f"{plugin_url}/load_config", data=json.dumps(payload), headers=headers)

    except requests.exceptions.RequestException as e:
        print("An error occurred loading config data:", e)
    except FileNotFoundError:
        print("No configuration found")
    except Exception as e:
        print(f"Error loading configuration: {e}")

    print("Starting BrightWS")
    bright_ws.start()


if __name__ == '__main__':
    main()
