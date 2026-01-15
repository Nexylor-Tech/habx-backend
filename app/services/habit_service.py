from datetime import datetime, timezone
from typing import List

from bson import ObjectId

from app.db import habits_collection, habits_logs_collection


async def get_habits(workspace_id: str) -> List[dict]:
    habits = []
    async for habit in habits_collection.find({"workspace_id": ObjectId(workspace_id)}):
        habits.append(habit)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    habit_ids = [h["_id"] for h in habits]

    logs = await habits_logs_collection.find(
        {"habit_id": {"$in": habit_ids}, "date": today}
    ).to_list(None)

    log_map = {str(log["habit_id"]): log["status"] for log in logs}

    for h in habits:
        h["today_habits"] = log_map.get(str(h["_id"]))
    return habits


async def create_habit(habit, workspace_id: str):
    new_habit = {
        "workspace_id": ObjectId(workspace_id),
        "title": habit["title"],
        "category": habit["category"],
        "icon": habit.get("icon", "activity"),
        "completion_count": 0,
        "skip_count": 0,
    }
    result = await habits_collection.insert_one(new_habit)
    return await habits_collection.find_one({"_id": result.inserted_id})


async def update_habit(
    habit_id: str, completion_count: int, skip_count: int, user_id: ObjectId
) -> None:
    await habits_collection.update_one(
        {"_id": ObjectId(habit_id), "user_id": user_id},
        {"$set": {"completion_count": completion_count, "skip_count": skip_count}},
    )
