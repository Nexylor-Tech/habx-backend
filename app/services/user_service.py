from datetime import datetime

from fastapi import HTTPException

from app.db import user_collection
from app.security import hash_password, verify_password


async def register_user(email: str, original_password: str, goal: str):
    if await user_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    await user_collection.insert_one(
        {
            "email": email,
            "password": hash_password(original_password),
            "goal": goal,
            "is_premium": False,
            "created_at": datetime.now(),
        }
    )


async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
