from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#@app.get("/pull")
def pull_container():
    subprocess.run("docker pull nginx", shell=True)
    return {"Hello": "World"}


#@app.get("/run")
def run_container():
    subprocess.run("docker run --name nginx nginx", shell=True)
    return {"Hello": "World"}

#@app.get("/stop")
def start_container():
    subprocess.run("docker stop nginx", shell=True)
    subprocess.run("docker rm nginx", shell=True)

