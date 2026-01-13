from fastapi import APIRouter, Response

from app.models.user import AuthResponse, LoginRequest, UserCreate
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(data: UserCreate, res: Response):
    return await user_service.register_user(data.email, data.password, data.goal)


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, res: Response):
    return await user_service.authenticate_user(data.email, data.password)
