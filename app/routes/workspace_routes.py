from typing import List

from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.workspace import WorkspaceCreate, WorkspaceResponse
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
