from bson import ObjectId

from app.tasks import schemas as task_schemas

from . import schemas
from .autochecker import AutoChecker, submit_code


async def get_attempt(db, attempt_id: str):
    return await db['attempts'].find_one({"_id": ObjectId(attempt_id)})


async def create_attempt(db, task: task_schemas.Task, attempt: schemas.AttemptRequest):
    ac = AutoChecker(task, attempt.text)
    attempt_details = submit_code(
        ac.generate_full_attempt(), ac.expected_output())
    attempt_details['task_id'] = task.id
    new_attempt = await db['attempts'].insert_one(attempt_details)
    created_attempt = await db['attempts'].find_one({"_id": new_attempt.inserted_id})
    return created_attempt


async def create_correct_attempt(db, task: task_schemas.Task, attempt: schemas.AttemptRequest):
    correct_attempt_file_path = "app/data/example_attempt_correct.py"
    with open(correct_attempt_file_path, "r") as correct_attempt_file:
        attempt_text = correct_attempt_file.read()

    ac = AutoChecker(task, attempt_text)
    attempt_details = submit_code(
        ac.generate_full_attempt(), ac.expected_output())
    attempt_details['task_id'] = task.id
    new_attempt = await db['attempts'].insert_one(attempt_details)
    created_attempt = await db['attempts'].find_one({"_id": new_attempt.inserted_id})
    return created_attempt
