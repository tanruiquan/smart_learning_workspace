# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    tags: list[str]


class Question(BaseModel):
    question_id: int
    title: str
    description: str
    tags: list[str]


class SolutionRequest(BaseModel):
    question_id: int


class Solution(BaseModel):
    solution_id: int
    question_id: int
    content: str


class AttemptRequest(BaseModel):
    question_id: int
    content: str


class Attempt(BaseModel):
    attempt_id: int
    question_id: int
    content: str
    is_correct: bool
    attempt_datetime: datetime


class FeedbackRequest(BaseModel):
    attempt_id: int


class Feedback(BaseModel):
    feedback_id: int
    attempt_id: int
    content: str
    feedback_datetime: datetime
