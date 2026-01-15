from typing import List

from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate
from app.services import workspace_service

router = APIRouter(prefix="/workspaces", tags=["habits"])


@router.get("/", response_model=List[WorkspaceResponse])
async def get_workspaces(current_user: dict = Depends(auth.get_current_user)):
    return await workspace_service.get_workspace(current_user["_id"])


@router.post("/", response_model=WorkspaceResponse)
async def create_workspace(
    ws: WorkspaceCreate, current_user: dict = Depends(auth.get_current_user)
):
    return await workspace_service.create_workspace(ws, current_user)


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: str,
    update: WorkspaceUpdate,
    current_user: dict = Depends(auth.get_current_user),
):
    return await workspace_service.update_workspace(
        workspace_id, update.model_dump(), current_user
    )
