from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.tasks import schemas as task_schemas
from app.tasks import service as task_service

from . import schemas, service

router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{attempt_id}", response_model_by_alias=False)
async def read_attempt(attempt_id: str, db=Depends(get_db)) -> schemas.Attempt:
    if (attempt := await service.get_attempt(db, attempt_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Attempt {attempt_id} not found")
    return attempt


@router.post("", response_model_by_alias=False)
async def create_attempt(attempt: schemas.AttemptRequest, db=Depends(get_db)) -> schemas.Attempt:
    if (task := await task_service.get_task(db, attempt.task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to create attempt. Task {attempt.task_id} not found")
    task = task_schemas.Task(**task)
    return await service.create_attempt(db, task, attempt)


@router.post("/test", response_model_by_alias=False)
async def test_create_attempt(task_id: str, is_correct: bool, db=Depends(get_db)) -> schemas.Attempt:
    if (task := await task_service.get_task(db, task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unable to create attempt. Task {task_id} not found")
    task = task_schemas.Task(**task)
    return await service.create_correct_attempt(db, task) if is_correct else await service.create_wrong_attempt(db, task)
