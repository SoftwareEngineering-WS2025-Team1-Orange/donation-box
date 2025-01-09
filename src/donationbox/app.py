from bright_ws.config.config import BrightConfig
from bright_ws.core.bright_ws import BrightWs
from donationbox.routes.config_route import config_router
from utils.settings import settings

from lifecycle.lifecycle import lifecycle
from routes.auth_route import auth_router
from routes.status_route import status_router
from routes.deploy_miner_route import deploy_router

running = False

#mining command:
#"docker run -itd --restart=always -e POOL_URL=pool.hashvault.pro:80 -e "POOL_USER="
#                   "41fLkHicU9w9a7mNpfxk13NxqB2FrzFc5HSnbDn1NUPwXy6dkkUgsyQVUBZ7qweyP19BWdMYJ4oq4D2SJ1eexPTv9MLCvQ3 "
#                   "--name monero pmietlicki/monero-miner", shell=True)


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
    bright_ws.start()


if __name__ == "__main__":
    main()
