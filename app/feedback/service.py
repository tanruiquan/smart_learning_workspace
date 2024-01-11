from datetime import datetime

from bson import ObjectId

from app.attempts import schemas as attempt_schemas
from app.tasks import schemas as task_schemas

from .utils import generate_trace, compare_trace


async def get_feedback(db, feedback_id: str):
    return await db['feedback'].find_one({"_id": ObjectId(feedback_id)})


def generate_feedback(task: task_schemas.Task, attempt: attempt_schemas.Attempt):
    # Get attempt model
    exec(attempt.text)
    attempt_model = locals()['model']
    # Get solution model
    exec(task.solution_text)
    solution_model = locals()['model']
    return "\n".join(compare_trace(generate_trace(attempt_model), generate_trace(solution_model)))


async def create_feedback(db, task: task_schemas.Task, attempt: attempt_schemas.Attempt):
    if attempt.status.description == "Accepted":
        content = "Great job! Your solution is correct."
    elif attempt.status.description == "Wrong Answer":
        content = generate_feedback(task, attempt)
        # content = "Your solution is incorrect."
    else:
        # Runtime error
        content = attempt.stderr
    new_feedback = await db['feedback'].insert_one({"task_id": task.id, "attempt_id": attempt.id, "content": content, "created_at": datetime.now()})
    created_feedback = await db['feedback'].find_one({"_id": new_feedback.inserted_id})
    return created_feedback
