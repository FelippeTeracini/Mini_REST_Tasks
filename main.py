from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks_dictionary = {1: {
    "title": "titulo 1",
    "description": "teste 1",
    "done": False
},
    2: {
    "title": "titulo 2",
    "description": "teste 2",
    "done": True
}}


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
    last_id = sorted(key)[-1]
    task_id = last_id + 1
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
    tasks_dictionary[task_id]["title"] = title
    tasks_dictionary[task_id]["description"] = description
    tasks_dictionary[task_id]["done"] = done
    return tasks_dictionary[task_id]


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    tasks_dictionary.pop(task_id)
    return tasks_dictionary


@app.get("/healthcheck")
def read_health():
    return
