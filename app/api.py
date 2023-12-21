# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import inspect
import logging
import os
from collections import defaultdict

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from . import crud, schemas
from .database import client
from .modules.autochecker import (AutoChecker, get_submission_details,
                                  submit_code)
from .modules.templates import TemplateMLP, TemplateRNN

logging.basicConfig(level=logging.DEBUG, filename="app/app.log", filemode="w")


app = FastAPI(
    title="Smart learning workspace",
    version="1.0",
    description="The backend repository for the smart learning workspace",
)


def get_db():
    return client.get_database("smart-learning-workspace")


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/docs")


@app.get("/tasks/{task_id}", tags=["Tasks"], response_model_by_alias=False)
async def read_task(task_id: str, db=Depends(get_db)) -> schemas.Task:
    if (task := await crud.get_task(db, task_id)) is not None:
        return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", tags=["Tasks"], response_model_by_alias=False)
async def create_task(task: schemas.TaskRequest, db=Depends(get_db)) -> schemas.Task:
    import json

    # Specify the path to your JSON file
    json_file_path = "app/data/example_task.json"

    # Read data from the JSON file
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        task = json.load(json_file)

    return await crud.create_task(db, schemas.TaskCreate(**task))


@app.get("/questions/{question_id}", tags=["Tasks"])
async def read_question(question_id: int, db=Depends(get_db)) -> schemas.Question:
    if (question := await crud.get_question(db, question_id)) is not None:
        return question
    raise HTTPException(
        status_code=404, detail=f"Question {question_id} not found")


@app.post("/questions", tags=["Tasks"], response_model_by_alias=False)
async def create_question(question: schemas.QuestionRequest, db=Depends(get_db)) -> schemas.Question:
    QUESTION1 = {"question_id": "1", "title": "Question title",
                 "description": "Question description", "tags": ["tag1", "tag2"]}
    return await crud.create_question(db, schemas.QuestionCreate(**QUESTION1))


@app.get("/solutions/{solution_id}", tags=["Tasks"])
async def read_solution(solution_id: int, db=Depends(get_db)) -> schemas.Solution:
    if (solution := await crud.get_solution(db, solution_id)) is not None:
        return solution
    raise HTTPException(
        status_code=404, detail=f"Solution {solution_id} not found")


@app.post("/solutions", tags=["Tasks"])
async def create_solution(solution: schemas.SolutionRequest, db=Depends(get_db)) -> schemas.Solution:
    if solution.type == "MLP":
        template = TemplateMLP(**solution.params)
    elif solution.type == "RNN":
        template = TemplateRNN(**solution.params)
    content = inspect.getsource(template)
    return await crud.create_solution(db, schemas.SolutionCreate(question_id=solution.question_id, type=solution.type, params=solution.params, content=content))


@app.get("/attempts/{attempt_id}", tags=["Attempts"], response_model_by_alias=False)
async def read_attempt(attempt_id: str, db=Depends(get_db)) -> schemas.Attempt:
    if (attempt := await crud.get_attempt(db, attempt_id)) is not None:
        return attempt
    raise HTTPException(
        status_code=404, detail=f"Attempt {attempt_id} not found")


@app.post("/attempts", tags=["Attempts"], response_model_by_alias=False)
async def create_attempt(attempt: schemas.AttemptRequest, db=Depends(get_db)) -> schemas.Attempt:
    if (task := await crud.get_task(db, attempt.task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Task {attempt.task_id} not found")
    logging.info(f"api:create_attempt: {task}")
    ac = AutoChecker(task, attempt.text)
    attempt_details = submit_code(
        ac.generate_full_attempt(), ac.expected_output())
    attributes = {key: value for key, value in attempt_details.items() if key in [
        "id", "question_id", "stdout", "time", "memory", "stderr", "token", "compile_output", "message", "created_at", "finished_at"]}
    attributes["status_id"] = attempt_details["status"]["id"]
    attributes["status_description"] = attempt_details["status"]["description"]
    attributes["task_id"] = attempt.task_id
    return await crud.create_attempt(db, schemas.AttemptCreate(**attributes))


@app.get("feedback/{feedback_id}", tags=["Feedback"])
async def read_feedback(feedback_id: int, db=Depends(get_db)) -> schemas.Feedback:
    return {"feedback_id": feedback_id, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}


@app.post("/feedback", tags=["Feedback"])
async def create_feedback(feedback: schemas.FeedbackRequest, db=Depends(get_db)) -> schemas.Feedback:
    return {"feedback_id": 1, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}
