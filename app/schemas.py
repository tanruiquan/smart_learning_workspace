from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class TemplateType(str, Enum):
    mlp = "MLP"
    rnn = "RNN"


class TaskRequest(BaseModel):
    pass


class TaskBase(BaseModel):
    title: str
    description: str
    tags: list[str]
    template_type: TemplateType
    solution_params: dict
    solution_text: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: PyObjectId = Field(..., alias="_id")


class QuestionRequest(BaseModel):
    tags: list[str]


class QuestionBase(BaseModel):
    title: str
    description: str
    tags: list[str]


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: PyObjectId = Field(..., alias="_id")


class SolutionBase(BaseModel):
    question_id: str
    type: TemplateType
    params: dict


class SolutionRequest(SolutionBase):
    pass


class SolutionCreate(SolutionBase):
    content: str


class Solution(SolutionBase):
    id: PyObjectId = Field(..., alias="_id")


class AttemptRequest(BaseModel):
    task_id: str
    text: str


class AttemptBase(BaseModel):
    task_id: str
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


class Attempt(AttemptBase):
    id: PyObjectId = Field(..., alias="_id")


class FeedbackRequest(BaseModel):
    attempt_id: str


class Feedback(BaseModel):
    feedback_id: str
    attempt_id: str
    content: str
    feedback_datetime: datetime
