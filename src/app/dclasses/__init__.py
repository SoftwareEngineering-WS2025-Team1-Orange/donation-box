from dataclasses import dataclass
from typing import Optional, Dict
from enum import Enum

@dataclass
class Event:
    event: str
    data: dict

    @staticmethod
    def from_dict(data: dict):
        return Event(data["event"], data["data"])

class AuthResponseEnum(str, Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'

class StatusUpdateResponseEnum(str, Enum):
    CURRENTLY_MINING = 'currently_mining'
    ERR_READY_FOR_MINING = 'ERR_ready_for_mining'
    ERR_NOT_READY_FOR_MINING = 'ERR_not_ready_for_mining'
    ERR_ERROR = 'ERR_error'

class StartMiningResponseEnum(str, Enum):
    STARTED_MINING = 'started_mining'
    ERR_IMAGE_NOT_FOUND = 'ERR_image_not_found'
    ERR_COULD_NOT_START_CONTAINER = 'ERR_could_not_start_container'
    ERR_CONNECTION_TO_MINING_POOL_FAILED = 'ERR_connection_to_mining_pool_failed'
    ERR_AUTHENTICATION_ON_MINING_POOL_FAILED = 'ERR_authentication_on_mining_pool_failed'
    ERR_OTHER = 'ERR_other'

class StopMiningResponseEnum(str, Enum):
    STOPPED_MINING = 'stopped_mining'
    ERR_CONTAINER_NOT_RUNNING = 'ERR_container_not_running'
    ERR_OTHER = 'ERR_other'

@dataclass
class AuthRequest:
    username: str
    password: str

@dataclass
class AuthResponse:
    success: bool
    response: AuthResponseEnum

@dataclass
class StatusUpdateResponse:
    success: bool
    response: StatusUpdateResponseEnum

@dataclass
class StartMiningRequest:
    imageName: str
    containerName: str
    environmentVars: Optional[Dict[str, str]]

@dataclass
class StopMiningRequest:
    containerName: str

@dataclass
class StartMiningResponse:
    success: bool
    response: StartMiningResponseEnum

@dataclass
class StopMiningResponse:
    status: bool
    response: StopMiningResponseEnum