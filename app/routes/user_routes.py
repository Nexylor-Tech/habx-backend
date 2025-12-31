from fastapi import APIRouter, Depends

from app.deps import auth

router = APIRouter(prefix="/me", tags=["Users"])


@router.get("/")
async def get_me(current_user: dict = Depends(auth.get_current_user)):
    return {
        "email": current_user["email"],
        "goal": current_user.get("goal", "Not Set"),
        "habits": current_user.get("is_premium", False),
    }
