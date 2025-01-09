import json
from datetime import datetime
from bright_ws import Router
import requests
from dclasses import StatusUpdateResponse, SolarStatusUpdateResponse, Production, Consumption
from utils import docker_manager
from utils import settings
from websocket import WebSocketApp


status_router = Router()


def parse_solar_status_update_response(data: str) -> SolarStatusUpdateResponse:
    parsed_json = json.loads(data)

    production = Production(
        solar=parsed_json["production"]["solar"],
        add=parsed_json["production"]["add"],
        grid=parsed_json["production"]["grid"]
    )

    consumption = Consumption(
        battery=parsed_json["consumption"]["battery"],
        house=parsed_json["consumption"]["house"],
        wallbox=parsed_json["consumption"]["wallbox"]
    )

    return SolarStatusUpdateResponse(
        sysStatus=parsed_json["sysStatus"],
        stateOfCharge=parsed_json["stateOfCharge"],
        production=production,
        consumption=consumption
    )


@status_router.route(event="statusRequest")
def status_update(message: dict, ws: WebSocketApp) ->  StatusUpdateResponse:

    container_port = docker_manager.get_container_port('pluginContainer')
    poll_url = f"http://localhost:{container_port}/poll"

    staus_update_response = StatusUpdateResponse(time=datetime.now().isoformat(),
                                                 solar=SolarStatusUpdateResponse(),
                                                 container={})
    try:
        payload = {
            "passkey": settings.passkey,
        }

        headers = {
            "Content-Type": "application/json"
        }
        poll_response = requests.post(poll_url, data=json.dumps(payload), headers=headers)

        if poll_response.status_code == 200:
            print("Success:", poll_response.status_code)
            staus_update_response.solar = parse_solar_status_update_response(poll_response.text)
        else:
            print("Failed with status code:", poll_response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    for container_name in docker_manager.get_monitored_containers():
        staus_update_response.container[container_name] = docker_manager.get_container_status(container_name)
    return staus_update_response
