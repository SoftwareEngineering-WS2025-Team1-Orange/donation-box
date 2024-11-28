from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pull")
def read_root():
    subprocess.run("docker pull nginx", shell=True)
    return {"Hello": "World"}


@app.get("/run")
def read_root():
    subprocess.run("docker run --name nginx nginx", shell=True)
    return {"Hello": "World"}

@app.get("/stop")
def read_root():
    subprocess.run("docker stop nginx", shell=True)
    subprocess.run("docker rm nginx", shell=True)

