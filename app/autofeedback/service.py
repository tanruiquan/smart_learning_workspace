from datetime import datetime

from bson import ObjectId

from app.schemas import Attempt, Task

from .client import Client


async def get_feedback(db, feedback_id: str):
    return await db['feedbacks'].find_one({"_id": ObjectId(feedback_id)})


async def create_feedback(db, task: Task, attempt: Attempt):
    if attempt.status_description == "Accepted":
        content = "Great job! Your solution is correct."
    else:
        content = "Your solution is incorrect."
    new_feedback = await db['feedbacks'].insert_one({"task_id": task.id, "attempt_id": attempt.id, "content": content, "created_at": datetime.now()})
    created_feedback = await db['feedbacks'].find_one({"_id": new_feedback.inserted_id})
    return created_feedback
