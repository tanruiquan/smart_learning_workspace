# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import os
import uuid
from collections import defaultdict

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import Body, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.models import (Attempt, AttemptRequest, Feedback, FeedbackRequest,
                        Question, QuestionRequest, Solution, SolutionRequest)
from app.modules.autochecker import get_submission_details, submit_code

logging.basicConfig(level=logging.DEBUG, filename="app/app.log", filemode="w")

app = FastAPI(
    title="Smart learning workspace",
    version="1.0",
    description="The backend repository for the smart learning workspace",
)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/docs")


@app.get("/questions/{question_id}", tags=["Tasks"])
def read_question(question_id: int) -> Question:
    return {"question_id": question_id, "title": "Question title", "description": "Question description", "tags": ["tag1", "tag2"]}


@app.post("/questions", tags=["Tasks"])
def create_question(question: QuestionRequest) -> Question:
    return {"question_id": 1, "title": "Question title", "description": "Question description", "tags": ["tag1", "tag2"]}


@app.get("/solutions/{solution_id}", tags=["Tasks"])
def read_solution(solution_id: int) -> Solution:
    return {"solution_id": solution_id, "question_id": 1, "content": "Solution content"}


@app.post("/solutions", tags=["Tasks"])
def create_solution(solution: SolutionRequest) -> Solution:
    return {"solution_id": 1, "question_id": 1, "content": "Solution content"}


@app.get("/attempts/{attempt_id}", tags=["Attempts"])
def read_attempt(attempt_id: int) -> Attempt:
    return {"attempt_id": attempt_id, "question_id": 1, "content": "Attempt content", "is_correct": True, "attempt_datetime": "2021-01-01T00:00:00Z"}


@app.post("/attempts", tags=["Attempts"])
def create_attempt(attempt: AttemptRequest) -> Attempt:
    response = submit_code(attempt.content)
    response["attempt_id"] = str(uuid.uuid4())
    response["question_id"] = attempt.question_id
    return response


@app.get("feedback/{feedback_id}", tags=["Feedback"])
def read_feedback(feedback_id: int) -> Feedback:
    return {"feedback_id": feedback_id, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}


@app.post("/feedback", tags=["Feedback"])
def create_feedback(feedback: FeedbackRequest) -> Feedback:
    return {"feedback_id": 1, "attempt_id": 1, "content": "Feedback content", "feedback_datetime": "2021-01-01T00:00:00Z"}
