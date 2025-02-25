from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List


class StartContainerResponseEnum(str, Enum):
    STARTED_CONTAINER = 'started_container'
    ERR_CONTAINER_ALREADY_RUNNING = 'ERR_container_already_running'
    ERR_IMAGE_NOT_FOUND = 'ERR_image_not_found'
    ERR_COULD_NOT_START_CONTAINER = 'ERR_could_not_start_container'


class StopContainerResponseEnum(str, Enum):
    STOPPED_CONTAINER = 'stopped_container'
    ERR_CONTAINER_NOT_RUNNING = 'ERR_container_not_running'
    ERR_OTHER = 'ERR_other'


class ContainerStatusMessageEnum(str, Enum):
    RUNNING = 'RUNNING'
    CRASHED = 'CRASHED'
    FINISHED = 'FINISHED'
    NOT_FOUND = 'NOT_FOUND'
    OK = 'OK'
    ERROR = 'ERROR'
    PENDING = 'PENDING'


class ContainerStatusCodeEnum(int, Enum):
    RUNNING = 0
    CRASHED = 1
    FINISHED = 2
    NOT_FOUND = 3
    OK = 100
    ERROR = 101
    PENDING = 102


@dataclass
class ContainerStatus:
    containerName: str
    statusCode: int
    statusMsg: ContainerStatusMessageEnum


@dataclass
class AuthRequest:
    username: str
    password: str


@dataclass
class AuthResponse:
    success: bool
    monitored_containers: List[str]


@dataclass
class Production:
    solar: int = 0
    add: int = 0
    grid: int = 0


@dataclass
class Consumption:
    battery: int = 0
    house: int = 0
    wallbox: int = 0


@dataclass
class SolarStatusUpdateResponse:
    sysStatus: int = 0
    stateOfCharge: int = 0
    production: Production = Production()
    consumption: Consumption = Consumption()


@dataclass
class StatusUpdateResponse:
    time: str
    power_supply: SolarStatusUpdateResponse
    container: List[ContainerStatus]


@dataclass
class StartContainerRequest:
    imageName: str
    containerName: str
    environmentVars: Optional[Dict[str, str]]


@dataclass
class StopContainerRequest:
    containerName: str


@dataclass
class StartContainerResponse:
    success: bool
    response: StartContainerResponseEnum


@dataclass
class StopContainerResponse:
    status: bool
    response: StopContainerResponseEnum


@dataclass
class AddConfigurationRequest:
    plugin_image_name: str
    plugin_configuration: Optional[Dict[str, str]]


@dataclass
class AddConfigurationResponse:
    success: bool


@dataclass
class StoredConfiguration:
    image_name: str
    port: Dict[str, str]
    plugin_configuration: Dict[str, str]


@dataclass
class AddErrorResponse:
    containerName: str
    statusCode: int
    statusMsg: str
