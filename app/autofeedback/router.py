from fastapi import APIRouter, Depends

from app.crud import get_attempt, get_task
from app.database import get_db
from app.schemas import Attempt, Task

from . import service
from .schemas import Feedback, FeedbackRequest

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{feedback_id}", response_model_by_alias=False)
async def read_feedback(feedback_id: str, db=Depends(get_db)) -> Feedback:
    if (feedback := await crud.get_feedback(db, feedback_id)) is not None:
        return feedback
    raise HTTPException(
        status_code=404, detail=f"Feedback {feedback_id} not found")


@router.post("", response_model_by_alias=False)
async def create_feedback(feedback: FeedbackRequest, db=Depends(get_db)) -> Feedback:
    if (attempt := await get_attempt(db, feedback.attempt_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to generate feedback. Attempt {feedback.attempt_id} not found")
    attempt = Attempt(**attempt)

    if (task := await get_task(db, attempt.task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to generate feedback. Task {attempt.task_id} not found")
    task = Task(**task)

    return await service.create_feedback(db, task, attempt)
