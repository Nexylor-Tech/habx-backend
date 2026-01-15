from typing import List

from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(current_user: dict = Depends(auth.get_current_user)):
    tasks = await task_service.get_tasks(current_user["_id"])
    return tasks


@router.post("/")
async def create_task(
    task: TaskCreate, current_user: dict = Depends(auth.get_current_user)
):
    task = await task_service.create_task(task.model_dump(), current_user["_id"])
    return task


@router.patch("/{task_id}")
async def update_task(
    task_id: str,
    update: TaskUpdate,
    current_user: dict = Depends(auth.get_current_user),
):
    await task_service.update_task(task_id, update.completed, current_user["_id"])
    return {"message": "Task updated successfully"}
