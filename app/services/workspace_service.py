from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import HTTPException

from app.db import (
    analytics_cache,
    habits_collection,
    habits_logs_collection,
    tasks_collection,
    workspace_collection,
)


async def get_workspace(user: ObjectId):
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    workspace = []
    async for ws in workspace_collection.find({"user_id": user}):
        last_completed = ws.get("last_completed")
        if last_completed:
            last_completed = datetime.strptime(last_completed, "%Y-%m-%d").date()

            # If last completion was before yesterday, streak is broken
            if last_completed < yesterday:
                ws["streak"] = 0
                # Optional: Update DB to reflect broken streak immediately
                await workspace_collection.update_one(
                    {"_id": ws["_id"]}, {"$set": {"streak": 0}}
                )
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
        "streak": 0,
        "last_completed": None,
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


async def update_workspace(workspace_id: str, update: dict, user):
    workspace = await workspace_collection.find_one(
        {"_id": ObjectId(workspace_id), "user_id": ObjectId(user["_id"])}
    )

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    update_res = {k: v for k, v in update.items() if v is not None}

    if update_res:
        await workspace_collection.update_one(
            {"_id": ObjectId(workspace_id)}, {"$set": update_res}
        )
        workspace = await workspace_collection.find_one({"_id": ObjectId(workspace_id)})

    return workspace


async def delete_workspace(workspace_id: str, user_id: ObjectId) -> dict:
    ws_id = ObjectId(workspace_id)
    workspace = await workspace_collection.find_one({"_id": ws_id, "user_id": user_id})

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    await habits_collection.delete_many({"workspace_id": ws_id})
    await tasks_collection.delete_many({"workspace_id": ws_id})
    await habits_logs_collection.delete_many({"workspace_id": ws_id})
    await analytics_cache.delete_many({"workspace_id": ws_id})

    await workspace_collection.delete_one({"_id": ws_id})

    return {"message": "Workspace deleted successfully"}
