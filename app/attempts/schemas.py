from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas import PyObjectId


class Status(BaseModel):
    id: int
    description: str


class AttemptBase(BaseModel):
    task_id: str
    text: str


class AttemptRequest(AttemptBase):
    pass


class Attempt(AttemptBase):
    id: PyObjectId = Field(..., alias="_id")
    source_code: str
    stdout: str | None
    time: float
    memory: int
    stderr: str | None
    token: str
    compile_output: str | None
    message: str | None
    status: Status
    created_at: datetime
    finished_at: datetime
