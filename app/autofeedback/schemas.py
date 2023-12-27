from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from app.schemas import PyObjectId


class FeedbackRequest(BaseModel):
    attempt_id: str


class FeedbackBase(BaseModel):
    task_id: str
    attempt_id: str
    content: str
    created_at: datetime


class Feedback(FeedbackBase):
    id: PyObjectId = Field(..., alias="_id")
