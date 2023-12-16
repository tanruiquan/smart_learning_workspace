from datetime import datetime

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    tags: list[str]


class Question(BaseModel):
    question_id: str
    title: str
    description: str
    tags: list[str]


class SolutionRequest(BaseModel):
    question_id: str


class Solution(BaseModel):
    solution_id: str
    question_id: str
    content: str


class AttemptRequest(BaseModel):
    question_id: str
    content: str


class Attempt(BaseModel):
    id: str
    question_id: str
    stdout: str | None
    time: float
    memory: int
    stderr: str | None
    token: str
    compile_output: str | None
    message: str | None
    status_id: int
    status_description: str
    created_at: datetime
    finished_at: datetime

    class Config:
        orm_mode = True


class FeedbackRequest(BaseModel):
    attempt_id: str


class Feedback(BaseModel):
    feedback_id: str
    attempt_id: str
    content: str
    feedback_datetime: datetime
