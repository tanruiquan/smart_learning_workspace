
from bson import ObjectId

from . import schemas


async def get_task(db, task_id: str):
    return await db['tasks'].find_one({"_id": ObjectId(task_id)})


async def get_tasks(db):
    return await db['tasks'].find().to_list(length=100)


async def create_task(db, task: schemas.TaskCreate):
    import json

    json_file_path = "app/data/example_task.json"

    with open(json_file_path, "r") as json_file:
        task = json.load(json_file)

    new_task = await db['tasks'].insert_one(task)
    created_task = await db['tasks'].find_one({"_id": new_task.inserted_id})
    return created_task
