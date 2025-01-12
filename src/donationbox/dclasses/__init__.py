from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List


class StartContainerResponseEnum(str, Enum):
    STARTED_CONTAINER = 'started_container'
    ERR_CONTAINER_ALREADY_RUNNING = 'ERR_container_already_running'
    ERR_IMAGE_NOT_FOUND = 'ERR_image_not_found'
    ERR_COULD_NOT_START_CONTAINER = 'ERR_could_not_start_container'
    ERR_CONNECTION_TO_MINING_POOL_FAILED = 'ERR_connection_to_mining_pool_failed'
    ERR_AUTHENTICATION_ON_MINING_POOL_FAILED = 'ERR_authentication_on_mining_pool_failed'
    ERR_OTHER = 'ERR_other'


class StopContainerResponseEnum(str, Enum):
    STOPPED_CONTAINER = 'stopped_container'
    ERR_CONTAINER_NOT_RUNNING = 'ERR_container_not_running'
    ERR_OTHER = 'ERR_other'


class ContainerStatusEnum(str, Enum):
    RUNNING = 'RUNNING',
    FINISHED = 'FINISHED',
    CRASHED = 'CRASHED'
    NOT_FOUND = 'NOT_FOUND'
    ERROR = 'ERROR'


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
    solar: SolarStatusUpdateResponse
    container: Dict[str, ContainerStatusEnum]


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
    image_name: str
    plugin_configuration: Optional[Dict[str, str]]

@dataclass
class AddConfigurationResponse:
    success: bool

@dataclass
class StoredConfiguration:
    image_name: str
    port: Dict[str, str]
    plugin_configuration: Dict[str, str]