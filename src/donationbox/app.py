from bright_ws.config.config import BrightConfig
from bright_ws.core.bright_ws import BrightWs
from utils.settings import settings

from lifecycle.lifecycle import lifecycle
from routes.auth_route import auth_router
from routes.status_route import status_router
from routes.deploy_miner_route import deploy_router

running = False


bright_ws = BrightWs(config=BrightConfig(
    host_url=settings.mainframe_socket_url,
    lifecycle=[lifecycle],
    routes=[auth_router,
            status_router,
            deploy_router
            ],
))


def main():
    bright_ws.start()


if __name__ == "__main__":
    main()
