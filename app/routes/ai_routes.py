from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.ai import AnalyticsResponse, GenerateRequest, SuggestionResponse
from app.services import ai_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-suggestions", response_model=list[SuggestionResponse])
async def generate_suggestions(request: GenerateRequest):
    suggestions = ai_service.generate_habits(request.goal)
    return suggestions


@router.get("/analytics", response_model=AnalyticsResponse)
async def generate_analytics(current_user: dict = Depends(auth.get_current_user)):
    return await ai_service.generate_analytics(current_user)
