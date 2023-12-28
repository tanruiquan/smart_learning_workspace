from fastapi import APIRouter, Depends, HTTPException

from app.attempts import schemas as attempt_schemas
from app.attempts import service as attempt_service
from app.database import get_db
from app.tasks import schemas as task_schemas
from app.tasks import service as task_service

from . import schemas, service

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{feedback_id}", response_model_by_alias=False)
async def read_feedback(feedback_id: str, db=Depends(get_db)) -> schemas.Feedback:
    if (feedback := await service.get_feedback(db, feedback_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Feedback {feedback_id} not found")

    return feedback


@router.post("", response_model_by_alias=False)
async def create_feedback(feedback: schemas.FeedbackRequest, db=Depends(get_db)) -> schemas.Feedback:
    if (attempt := await attempt_service.get_attempt(db, feedback.attempt_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to generate feedback. Attempt {feedback.attempt_id} not found")
    attempt = attempt_schemas.Attempt(**attempt)

    if (task := await task_service.get_task(db, attempt.task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to generate feedback. Task {attempt.task_id} not found")
    task = task_schemas.Task(**task)

    return await service.create_feedback(db, task, attempt)
