from datetime import datetime

from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    name: str


class QuestionRequest(BaseModel):
    tags: list[str]


class Question(BaseModel):
    id: int
    title: str
    description: str
    tags: list[Tag]


class SolutionRequest(BaseModel):
    question_id: int


class Solution(BaseModel):
    solution_id: int
    question_id: int
    content: str


class AttemptRequest(BaseModel):
    question_id: int
    content: str


class AttemptBase(BaseModel):
    question_id: int
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


class AttemptCreate(AttemptBase):
    pass


class Attempt(BaseModel):
    id: int
    question_id: int
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
    attempt_id: int


class Feedback(BaseModel):
    feedback_id: int
    attempt_id: int
    content: str
    feedback_datetime: datetime
