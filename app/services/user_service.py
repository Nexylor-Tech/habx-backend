from datetime import datetime, timedelta, timezone
from typing import List

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


async def get_me(user_id: dict) -> dict:
    streak = user_id.get("streak", 0)
    last_completed = user_id.get("last_completed")
    if last_completed:
        last_completed = datetime.strptime(last_completed, "%Y-%m-%d").date()
        today = datetime.now(timezone.utc).date()
        yesterday = today - timedelta(days=1)

        # If last completion was before yesterday, streak is broken
        if last_completed < yesterday:
            streak = 0
            # Optional: Update DB to reflect broken streak immediately
            await user_collection.update_one({"_id": user_id}, {"$set": {"streak": 0}})

    created_at = user_id["created_at"]
    return {
        "email": user_id["email"],
        "goal": user_id.get("goal", "Not Set"),
        "isPremium": user_id.get("is_premium", False),
        "streak": streak,
        "created_at": created_at.isoformat() if created_at else None,
    }
