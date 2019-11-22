from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import uvicorn
import os
from bson.objectid import ObjectId

# db_ip = '172.31.23.100'
db_ip = os.getenv("DB_IP")
db_ip = "mongodb://" + db_ip + ":27017"

client = pymongo.MongoClient(db_ip)
db = client["cloudDatabase"]
tasks = db["tasks"]

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    done: bool


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/task")
async def read_tasks():
    tasks_list = {}
    tasks_list["Tasks"] = []
    for i in tasks.find():
        tasks_list["Tasks"].append(
            {"id": str(i["_id"]), "title": i["title"], "description": i["description"], "done": i["done"]})
    return tasks_list


@app.post("/task")
async def create_task(task: Task):
    new_task = {"title": task.title,
                "description": task.description, "done": task.done}
    tasks.insert_one(new_task)


@app.get("/task/{task_id}")
async def read_task(task_id: str):
    tasks_list = {}
    tasks_list["Tasks"] = []
    for i in tasks.find({"_id": ObjectId(task_id)}):
        tasks_list["Tasks"].append(
            {"id": i["_id"], "title": i["title"], "description": i["description"], "done": i["done"]})
    return tasks_list


@app.put("/task/{task_id}")
async def update_task(task_id: str, task: Task):
    tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {
                     "title": task.title, "description": task.description, "done": task.done}})


@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    tasks.remove({"_id": ObjectId(task_id)})


@app.get("/healthcheck")
async def read_health():
    return
