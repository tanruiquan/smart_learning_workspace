from datetime import datetime

from pydantic import BaseModel, Field

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
