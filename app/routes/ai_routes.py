from typing import List

from fastapi import APIRouter, Depends
from google.genai.types import Dict

from app.deps import auth
from app.models.ai import (
    AnalyticsResponse,
    GenerateRequest,
    SuggestionResponse,
    WeeklyAnalyticsResponse,
)
from app.services import ai_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-suggestions", response_model=list[SuggestionResponse])
async def generate_suggestions(
    request: GenerateRequest, user: dict = Depends(auth.get_current_user)
):
    suggestions = ai_service.generate_habits(request.goal, user)
    return suggestions


@router.get("/analytics", response_model=AnalyticsResponse)
async def generate_analytics(
    current_user: dict = Depends(auth.get_current_user),
    workspace_id: str = Depends(auth.get_current_workspace_id),
):
    return await ai_service.generate_analytics(current_user, workspace_id)


@router.get("/analytics/weekly", response_model=List[WeeklyAnalyticsResponse])
async def generate_insight_weekly(
    workspace_id: str = Depends(auth.get_current_workspace_id),
):
    return await ai_service.generate_insight_weekly(workspace_id)
