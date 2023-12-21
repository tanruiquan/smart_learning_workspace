import logging

from bson import ObjectId

from . import schemas


async def get_task(db, task_id: str):
    return await db['tasks'].find_one({"_id": ObjectId(task_id)})


async def create_task(db, task: schemas.TaskCreate):
    new_task = await db['tasks'].insert_one(task.dict())
    created_task = await db['tasks'].find_one({"_id": new_task.inserted_id})
    logging.info(f"Created task: {created_task}")
    return created_task


async def get_question(db, question_id: str):
    return await db['questions'].find_one({"_id": ObjectId(question_id)})


async def create_question(db, question: schemas.QuestionCreate):
    new_question = await db['questions'].insert_one(question.dict())
    created_question = await db['questions'].find_one({"_id": new_question.inserted_id})
    logging.info(f"Created question: {created_question}")
    return created_question


async def get_solution(db, solution_id: str):
    return await db['solutions'].find_one({"_id": ObjectId(solution_id)})


async def create_solution(db, solution: schemas.Solution):
    new_solution = await db['solutions'].insert_one(solution.dict())
    created_solution = await db['solutions'].find_one({"_id": new_solution.inserted_id})
    return created_solution


async def get_attempt(db, attempt_id: str):
    return await db['attempts'].find_one({"_id": ObjectId(attempt_id)})


async def create_attempt(db, attempt: schemas.AttemptCreate):
    new_attempt = await db['attempts'].insert_one(attempt.dict())
    created_attempt = await db['attempts'].find_one({"_id": new_attempt.inserted_id})
    return created_attempt


async def get_feedback(db, feedback_id: str):
    return await db['feedbacks'].find_one({"_id": ObjectId(feedback_id)})


async def create_feedback(db, feedback: schemas.Feedback):
    new_feedback = await db['feedbacks'].insert_one(feedback.dict())
    created_feedback = await db['feedbacks'].find_one({"_id": new_feedback.inserted_id})
    return created_feedback
