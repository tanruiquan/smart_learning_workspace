from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db

from . import schemas, service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model_by_alias=False)
async def read_tasks(db=Depends(get_db)) -> list[schemas.Task]:
    return await service.get_tasks(db)


@router.get("/{task_id}", response_model_by_alias=False)
async def read_task(task_id: str, db=Depends(get_db)) -> schemas.Task:
    if (task := await service.get_task(db, task_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Task {task_id} not found")
    return task


@router.post("", response_model_by_alias=False)
async def create_task(task: schemas.TaskRequest, db=Depends(get_db)) -> schemas.Task:
    return await service.create_task(db, task)
