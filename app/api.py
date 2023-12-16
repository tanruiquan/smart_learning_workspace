# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import os
import uuid
from collections import defaultdict

import uvicorn
from fastapi import Body, FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .modules.autochecker import get_submission_details, submit_code
from .database import SessionLocal, engine
from . import crud, models, schemas

logging.basicConfig(level=logging.DEBUG, filename="app/app.log", filemode="w")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart learning workspace",
    version="1.0",
    description="The backend repository for the smart learning workspace",
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/docs")


@app.get("/questions/{question_id}", tags=["Tasks"])
def read_question(question_id: int) -> schemas.Question:
    return {"question_id": question_id, "title": "Question title", "description": "Question description", "tags": ["tag1", "tag2"]}


@app.post("/questions", tags=["Tasks"])
def create_question(question: schemas.QuestionRequest) -> schemas.Question:
    return {"question_id": 1, "title": "Question title", "description": "Question description", "tags": ["tag1", "tag2"]}


@app.get("/solutions/{solution_id}", tags=["Tasks"])
def read_solution(solution_id: int) -> schemas.Solution:
    return {"solution_id": solution_id, "question_id": 1, "content": "Solution content"}


@app.post("/solutions", tags=["Tasks"])
def create_solution(solution: schemas.SolutionRequest) -> schemas.Solution:
    return {"solution_id": 1, "question_id": 1, "content": "Solution content"}


@app.get("/attempts/{attempt_id}", tags=["Attempts"])
def read_attempt(attempt_id: int) -> schemas.Attempt:
    return {"attempt_id": attempt_id, "question_id": 1, "content": "Attempt content", "is_correct": True, "attempt_datetime": "2021-01-01T00:00:00Z"}


@app.post("/attempts", tags=["Attempts"])
def create_attempt(attempt: schemas.AttemptRequest, db: Session = Depends(get_db)) -> schemas.Attempt:
    attempt_details = submit_code(attempt.content, "hello world")
    attributes = {key: value for key, value in attempt_details.items() if key in [
        "id", "question_id", "stdout", "time", "memory", "stderr", "token", "compile_output", "message", "created_at", "finished_at"]}
    attributes["status_id"] = attempt_details["status"]["id"]
    attributes["status_description"] = attempt_details["status"]["description"]
    attributes["id"] = str(uuid.uuid4())
    attributes["question_id"] = attempt.question_id
    return crud.create_attempt(db, schemas.Attempt(**attributes))


@app.get("feedback/{feedback_id}", tags=["Feedback"])
def read_feedback(feedback_id: int) -> schemas.Feedback:
    return {"feedback_id": feedback_id, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}


@app.post("/feedback", tags=["Feedback"])
def create_feedback(feedback: schemas.FeedbackRequest) -> schemas.Feedback:
    return {"feedback_id": 1, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}
