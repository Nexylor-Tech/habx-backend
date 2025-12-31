from fastapi import APIRouter
from app.models.ai import GenerateRequest, SuggestionResponse
from app.services import ai_service
router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/generate-suggestions", response_model=list[SuggestionResponse])
async def generate_suggestions(request: GenerateRequest):
    suggestions = ai_service.generate_habits(request.goal)
    return suggestions