from typing import List

from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(workspace_id: str = Depends(auth.get_current_workspace_id)):
    return await task_service.get_tasks(workspace_id)


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate, workspace_id: str = Depends(auth.get_current_workspace_id)
):
    return await task_service.create_task(task.model_dump(), workspace_id)


@router.patch("/{task_id}")
async def update_task(
    task_id: str,
    update: TaskUpdate,
):
    await task_service.update_task(task_id, update)
    return {"message": "Task updated successfully"}
