from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import uvicorn
import os
from bson.objectid import ObjectId

db_ip = os.getenv("DB_IP")
db_ip = 'mongodb://' + db_ip + ':27017/'
client = pymongo.MongoClient(db_ip)
db = client['cloudDatabase']
tasks = db['tasks']

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    done: bool


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task")
def read_tasks():
    tasks_list = {}
    for i in tasks.find():
        tasks_list[i['_id']] = {'title': i['title'],
                                'description': i['description'], 'done': i['done']}
    return tasks_list


@app.post("/task")
def create_task(task: Task):
    new_task = {'title': task.title,
                'description': task.description, 'done': task.done}
    tasks.insert_one(new_task)
    return new_task


@app.get("/task/{task_id}")
def read_task(task_id: int):
    found_task = tasks.find({'_id': ObjectId(task_id)})
    return_task = {'id': found_task['_id'], 'title': found_task['title'],
                   'description': found_task['description'], 'done': found_task['done']}
    return return_task


@app.put("/task/{task_id}")
def update_task(task_id: int, task: Task):
    tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {
                     'title': task.title, 'description': task.description, 'done': task.done}})


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    tasks.remove({'_id': ObjectId(task_id)})


@app.get("/healthcheck")
def read_health():
    return
