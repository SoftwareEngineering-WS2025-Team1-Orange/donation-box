import sys
from enum import Enum
from typing import Optional, Dict

import docker
from dclasses import StartContainerRequest, ContainerStatusEnum, ContainerStatus


class DockerManager:
    class StartContainerResult(Enum):
        SUCCESS = 0
        RESTARTED = 1
        ALREADY_RUNNING = 2
        IMAGE_NOT_FOUND = 3
        ERROR = 4

    class StopRemoveContainerResult(Enum):
        SUCCESS = 0
        CONTAINER_NOT_FOUND = 1
        ERROR = 2

    monitored_containers = []

    def __init__(self):
        self.client = docker.from_env()

    def get_monitored_containers(self):
        return self.monitored_containers

    def get_container_port(self, container_name, port_int='8000/tcp'):
        try:
            return self.client.containers.get(container_name).ports[port_int][0]['HostPort']
        except docker.errors.NotFound:
            print(f'get_container_port: Container {container_name} not found', file=sys.stderr)
            return None
        except KeyError:
            print(f'Port mapping for container {container_name} not found', file=sys.stderr)
            return None
        except Exception as e:
            print(f'An unexpected error occurred: {e}', file=sys.stderr)
            return None

    def add_monitored_container(self, container_name: str):
        self.monitored_containers.append(container_name)

    def start_container(self, request: StartContainerRequest,
                        port: Optional[Dict[str, str]] = None) -> StartContainerResult:
        try:
            if self.exists(request.containerName):
                if not self.monitored_containers.__contains__(request.containerName):
                    self.add_monitored_container(request.containerName)

                if self.get_container_status(request.containerName).status_message == ContainerStatusEnum.RUNNING:
                    return self.StartContainerResult.ALREADY_RUNNING

                self.client.containers.get(request.containerName).start()
                return self.StartContainerResult.RESTARTED

            if port:
                assert 'int' in port and 'ext' in port, "Port mapping must contain 'int' and 'ext' values"
                self.client.containers.run(
                    request.imageName,
                    name=request.containerName,
                    environment=request.environmentVars,
                    ports={port['int']: port['ext']},
                    detach=True,
                )
            else:
                self.client.containers.run(
                    request.imageName,
                    name=request.containerName,
                    environment=request.environmentVars,
                    detach=True,
                )

            self.add_monitored_container(request.containerName)
            return self.StartContainerResult.SUCCESS

        except docker.errors.ImageNotFound:
            print(f'start_container: Image {request.imageName} not found', file=sys.stderr)
            return self.StartContainerResult.IMAGE_NOT_FOUND
        except docker.errors.APIError as e:
            print(f'start_container: An error occurred: {e}', file=sys.stderr)
            return self.StartContainerResult.ERROR

    def stop_container(self, container_name: str) -> StopRemoveContainerResult:
        try:
            self.client.containers.get(container_name).stop()
            return self.StopRemoveContainerResult.SUCCESS
        except docker.errors.NotFound:
            print(f'stop_container: Container {container_name} not found', file=sys.stderr)
            return self.StopRemoveContainerResult.CONTAINER_NOT_FOUND
        except docker.errors.APIError as e:
            print(f'stop_container: An error occurred: {e}', file=sys.stderr)
            return self.StopRemoveContainerResult.ERROR

    def remove_container(self, container_name: str) -> StopRemoveContainerResult:
        self.stop_container(container_name)
        try:
            self.client.containers.get(container_name).remove()
            if self.monitored_containers.__contains__(container_name):
                self.monitored_containers.remove(container_name)
            return self.StopRemoveContainerResult.SUCCESS
        except docker.errors.NotFound:
            print(f'remove_container: Container {container_name} not found', file=sys.stderr)
            return self.StopRemoveContainerResult.CONTAINER_NOT_FOUND
        except docker.errors.APIError as e:
            print(f'stop_container: An error occurred: {e}', file=sys.stderr)
            return self.StopRemoveContainerResult.ERROR

    def get_container_status(self, container_name: str) -> ContainerStatus:
        try:
            container = self.client.containers.get(container_name)
            match container.status:
                case 'running':
                    return ContainerStatus(
                        containerName=container_name,
                        statusCode=0,
                        statusMsg=ContainerStatusEnum.RUNNING
                    )
                case 'exited':
                    exit_code = container.attrs['State']['ExitCode']
                    match exit_code:
                        case 0:
                            return ContainerStatus(
                                containerName=container_name,
                                statusCode=200,
                                statusMsg=ContainerStatusEnum.FINISHED
                            )
                        case ec:
                            return ContainerStatus(
                                containerName=container_name,
                                statusCode=ec,
                                statusMsg=ContainerStatusEnum.CRASHED
                            )
                case _:
                    raise docker.errors.APIError("Unknown container status")
        except docker.errors.NotFound:
            print(f'get_container_status: Container {container_name} not found', file=sys.stderr)
            return ContainerStatus(
                containerName=container_name,
                statusCode=404,
                statusMsg=ContainerStatusEnum.NOT_FOUND
            )
        except docker.errors.APIError as e:
            print(f'get_container_status: An error occurred: {e}', file=sys.stderr)
            return ContainerStatus(
                containerName=container_name,
                statusCode=500,
                statusMsg=ContainerStatusEnum.ERROR
            )

    def exists(self, container_name: str):
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False
        except docker.errors.APIError:
            return False


docker_manager = DockerManager()
