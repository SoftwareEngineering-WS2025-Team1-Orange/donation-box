import sys
import docker
from dclasses import StartMiningRequest, ContainerStatusEnum


class DockerManager:
    monitored_containers = []

    def __init__(self):
        self.client = docker.from_env()

    def get_monitored_containers(self):
        return self.monitored_containers

    def add_monitored_container(self, container_name: str):
        self.monitored_containers.append(container_name)

    def start_container(self, request: StartMiningRequest):
        try:
            if self.exists(request.containerName):
                self.client.containers.get(request.containerName).start()
                return self.client.containers.get(request.containerName)

            container = self.client.containers.run(
                request.imageName,
                name=request.containerName,
                environment=request.environmentVars,
                detach=True,
            )
            self.monitored_containers.append(request.containerName)
            return container
        except docker.errors.ImageNotFound:
            print(f'Image {request.imageName} not found', file=sys.stderr)
            return None
        except docker.errors.APIError:
            print('Error starting container: {e}', file=sys.stderr)
            return None

    def stop_container(self, request: StartMiningRequest):
        try:
            container = self.client.containers.get(request.containerName)
            container.stop()
            return True
        except docker.errors.NotFound:
            print(f'Container {request.containerName} not found', file=sys.stderr)
            return False
        except docker.errors.APIError as e:
            print(f'Error stopping container: {e}', file=sys.stderr)
            return False

    def remove_container(self, container_name: str):
        try:
            container = self.client.containers.get(container_name)
            container.remove()
            if self.monitored_containers.__contains__(container_name):
                self.monitored_containers.remove(container_name)
            print(f"Removed container {container_name}")
            return True
        except docker.errors.NotFound:
            print(f'Container {container_name} not found', file=sys.stderr)
            return False
        except docker.errors.APIError as e:
            print(f'Error removing container: {e}', file=sys.stderr)
            return False

    def get_container_status(self, container_name: str):
        try:
            container = self.client.containers.get(container_name)
            if container.status == 'running':
                return ContainerStatusEnum.RUNNING
            elif container.status == 'exited':
                exit_code = container.attrs['State']['ExitCode']
                if exit_code == 0:
                    return ContainerStatusEnum.FINISHED
                else:
                    return ContainerStatusEnum.CRASHED
            else:
                return ContainerStatusEnum.ERROR
        except docker.errors.NotFound:
            return ContainerStatusEnum.NOT_FOUND
        except docker.errors.APIError as e:
            print(f'Error getting container status: {e}', file=sys.stderr)
            return ContainerStatusEnum.ERROR

    def exists(self, container_name: str):
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False
        except docker.errors.APIError:
            return False


docker_manager = DockerManager()
