from datetime import timedelta

from fastapi import APIRouter, Response

from app.config import settings
from app.models.user import AuthResponse, LoginRequest, UserCreate
from app.security import create_access_token
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(data: UserCreate, res: Response):
    await user_service.register_user(data.email, data.password, data.goal)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.email}, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": data.email,
        "goal": data.goal,
    }


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, res: Response):
    user = await user_service.authenticate_user(data.email, data.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user["email"],
        "goal": user.get("goal"),
    }
