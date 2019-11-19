from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests
import sys
import getopt
import json

app = FastAPI()


class Server():
    address = sys.argv[2] + ':' + sys.argv[4]


argv = sys.argv[1:]
server_address = ''
PORT = 0

try:
    opts, args = getopt.getopt(
        argv, "h", ["server_address=", "port="])
except getopt.GetoptError:
    print(
        'redirection.py --server_address <server-address> --port <port>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '--server_address':
        server_address = arg
    elif opt == '--port':
        PORT = arg

server_address = server_address + ':' + PORT
Server.address = server_address
print("Server Address main: {}".format(Server.address))
PORT = int(PORT)


class Task(BaseModel):
    title: str
    description: str
    done: bool


@app.get("/")
def read_root():
    return requests.get(Server.address + '/').json()


@app.get("/task")
def read_tasks():
    return requests.get(Server.address + '/task').json()


@app.post("/task")
def create_task(task: Task):
    print("Task: {}".format(task.dict()))
    return requests.post(Server.address + '/task',
                         data=json.dumps(task.dict()))


@app.get("/task/{task_id}")
def read_task(task_id: int):
    return requests.get(Server.address + '/task/' + task_id).json()


@app.put("/task/{task_id}")
def update_task(task_id: int, task: Task):
    return requests.post(Server.address + '/task/' + task_id,
                         data=task)


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    return requests.delete(Server.address + '/task/' + task_id).json()


@app.get("/healthcheck")
def read_health():
    return requests.get(Server.address + '/healthcheck').json()


if __name__ == "__main__":
    uvicorn.run("redirection:app", host='0.0.0.0',
                port=PORT, log_level="info")
