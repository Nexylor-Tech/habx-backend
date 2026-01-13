from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException

from app.db import habits_collection, workspace_collection


async def get_workspace(user: ObjectId):
    workspace = []
    async for ws in workspace_collection.find({"user_id": user}):
        workspace.append(ws)

    return workspace


async def create_workspace(ws, user: dict):
    user_id = ObjectId(user["_id"])
    count = await workspace_collection.count_documents({"user_id": user_id})
    limit = user.get("workspace_limit", 1)

    if not count <= limit:
        raise HTTPException(
            status_code=403,
            detail="Workspace Limit rerached, please upgrade ur account to create more.",
        )

    new_workspace = {
        "user_id": user_id,
        "name": ws.name,
        "goal": ws.goal,
        "created_at": datetime.now(timezone.utc),
    }
    res = await workspace_collection.insert_one(new_workspace)

    if ws.initial_habits:
        habits_to_insert = [
            {
                "workspace_id": res.inserted_id,
                "title": h["title"],
                "category": h.get("category", "General"),
                "icon": h.get("icon", "activity"),
                "completion_count": 0,
                "skip_count": 0,
            }
            for h in ws.initial_habits
        ]
        if habits_to_insert:
            await habits_collection.insert_many(habits_to_insert)

    return {**new_workspace, "_id": res.inserted_id}
