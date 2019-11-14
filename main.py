from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

tasks_dictionary = {}


class Task(BaseModel):
    title: str
    description: str
    done: bool


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task")
def read_tasks():
    return tasks_dictionary


@app.post("/task")
def create_task(task: Task):
    key = tasks_dictionary.keys()
    key_list = sorted(key)
    if(len(key_list) != 0):
        last_id = key_list[-1]
        task_id = last_id + 1
    else:
        task_id = 1
    tasks_dictionary[task_id] = task
    return tasks_dictionary


@app.get("/task/{task_id}")
def read_task(task_id: int):
    return tasks_dictionary[task_id]


@app.put("/task/{task_id}")
def update_task(task_id: int, task: Task):
    title = task.title
    description = task.description
    done = task.done
    tasks_dictionary[task_id].title = title
    tasks_dictionary[task_id].description = description
    tasks_dictionary[task_id].done = done
    return tasks_dictionary[task_id]


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    tasks_dictionary.pop(task_id)
    return tasks_dictionary


@app.get("/healthcheck")
def read_health():
    return
