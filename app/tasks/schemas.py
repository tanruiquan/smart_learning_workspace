from enum import Enum

from pydantic import BaseModel, Field

from app.schemas import PyObjectId


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
