from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException

from app.config import settings
from app.db import user_collection, workspace_collection
from app.dodo_client import client
from app.logger_config import setting
from app.security import create_access_token, hash_password, verify_password


# create dodo customer during regisration
async def create_dodo_customer(dodo_email: str, dodo_name: str) -> Optional[str]:
    if not client.dodo_client:
        setting.logger.error("DODO_API_KEY is not set")
        return None

    try:
        res = await client.dodo_client.customers.create(
            email=dodo_email, name=dodo_name
        )
        if not res.customer_id:
            setting.logger.error(f"Failed to create dodo customer: {res}")
        return res.customer_id

    except Exception as e:
        setting.logger.error(f"Error creating dodo customer: {e}")
        return None


async def register_user(email: str, original_password: str, goal: str) -> dict:
    if await user_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    dodo_customer_id = await create_dodo_customer(email, email.split("@")[0])
    if not dodo_customer_id:
        raise HTTPException(status_code=500, detail="Failed to create DODO customer")
    res = await user_collection.insert_one(
        {
            "email": email,
            "password": hash_password(original_password),
            "is_premium": False,
            "created_at": datetime.now(),
            "subscription_tier": "free",
            "dodo_customer_id": dodo_customer_id,
            "ai_generation_count": 0,
            "ai_generation_limit": settings.AI_LIMITS["free"],
            "workspace_limit": settings.WORKSPACE_LIMITS["free"],
            "subscription_status": "active",
            "subscription_expiry": None,
        }
    )
    user_id = res.inserted_id
    new_workspace = {
        "user_id": user_id,
        "name": "My Workspace",
        "goal": goal,
        "created_at": datetime.now(timezone.utc),
        "streak": 0,
        "last_completed": None,
    }

    ws_res = await workspace_collection.insert_one(new_workspace)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email,
        "goal": goal,
        "subscription_tier": "free",
        "workspace_limit": settings.WORKSPACE_LIMITS["free"],
        "current_workspace_id": str(ws_res.inserted_id),
    }


async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    workspace = await workspace_collection.find_one({"user_id": user["_id"]})
    ws_id = str(workspace["_id"] if workspace else "")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user["email"],
        "goal": workspace["goal"] if workspace else "",
        "subscription_tier": user.get("subscription_tier", "free"),
        "workspace_limit": user.get("workspace_limit", 1),
        "current_workspace_id": ws_id,
    }


async def get_me(user: dict) -> dict:
    # created_at = user_id["created_at"]

    expiry = user.get("subscription_expiry")
    if expiry and isinstance(expiry, str):
        expiry_date = datetime.fromisoformat(expiry)
        if (
            datetime.now(timezone.utc) > expiry_date
            and user.get("subscription_tier") != "free"
        ):
            await user_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "subscription_tier": "free",
                    "is_premium": False,
                    "subscription_status": "expired",
                    "ai_generation_limit": settings.AI_LIMITS["free"],
                    "workspace_limit": settings.WORKSPACE_LIMITS["free"],
                }},
            )
            user["subscription_tier"] = "free"
            user["workspace_limit"] = settings.WORKSPACE_LIMITS["free"]
    created_at = user.get("created_at")

    return {
        "email": user["email"],
        "subscriptionTier": user.get("subscription_tier", "free"),
        "isPremium": user.get("is_premium", False),
        "subscriptionStatus": user.get("subscription_status", "active"),
        "subscriptionExpiry": user.get("subscription_expiry", None),
        "aiUsage": user.get("ai_generation_count", 0),
        "aiLimit": user.get("ai_generation_limit", 10),
        "workspaceLimit": user.get("workspace_limit", 1),
        "created_at": created_at.isoformat() if created_at else None,
    }
