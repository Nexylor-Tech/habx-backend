from fastapi import APIRouter, Depends

from app.deps import auth
from app.services import user_service

router = APIRouter(prefix="/me", tags=["Users"])


@router.get("/")
async def get_me(current_user: dict = Depends(auth.get_current_user)):
    return await user_service.get_me(current_user)
