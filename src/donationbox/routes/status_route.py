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
def status_update(message: dict, ws: WebSocketApp) -> StatusUpdateResponse:
    status_update_response = StatusUpdateResponse(time=datetime.now().isoformat(),
                                                  power_supply=SolarStatusUpdateResponse(),
                                                  container=[])

    for container_name in docker_manager.get_monitored_containers():
        status_update_response.container.append(
            docker_manager.get_container_status(container_name)
        )

    container_port = docker_manager.get_container_port('pluginContainer')
    if container_port is None:
        return status_update_response
    poll_url = f"http://localhost:{container_port}/poll"

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
            status_update_response.power_supply = parse_solar_status_update_response(poll_response.text)
            return status_update_response
        else:
            ws.send(json.dumps({"event": "addErrorResponse",
                                "data": {"containerName": "pluginContainer",
                                         "statusCode": poll_response.status_code,
                                         "statusMessage": "Error: Cannot poll"}}))
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    return status_update_response
