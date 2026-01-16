from datetime import datetime, timedelta, timezone
from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException

from app.db import (
    habits_collection,
    habits_logs_collection,
    user_collection,
    workspace_collection,
)
from app.logger_config import setting


async def log_habit(habit_id: str, log: dict, user: dict) -> dict:
    habit = await habits_collection.find_one({"_id": ObjectId(habit_id)})
    workspace = await workspace_collection.find_one({"_id": habit["workspace_id"]})

    if log["status"] not in [0, 1]:
        setting.logger.error("Status must be integer , 0 or 1")

    if not workspace or workspace["user_id"] != user["_id"]:
        raise HTTPException(status_code=404, detail="Unauthorized")

    existing = await habits_logs_collection.find_one(
        {"habit_id": ObjectId(habit_id), "date": log["date"]}
    )
    if existing:
        if existing["status"] != log["status"]:
            if log["status"] == 1:
                inc = {"completion_count": 1, "skip_count": -1}
            else:
                inc = {"completion_count": -1, "skip_count": 1}

            await habits_collection.update_one(
                {"_id": ObjectId(habit_id)}, {"$inc": inc}
            )
            await habits_logs_collection.update_one(
                {"_id": existing["_id"]}, {"$set": {"status": log["status"]}}
            )
    else:
        await habits_logs_collection.insert_one(
            {
                "habit_id": ObjectId(habit_id),
                "date": log["date"],
                "status": log["status"],
                "workspace_id": habit["workspace_id"],
            }
        )
        field_to_inc = "completion_count" if log["status"] == 1 else "skip_count"

        await habits_collection.update_one(
            {"_id": ObjectId(habit_id)},
            {"$inc": {field_to_inc: 1}},
        )

        # user = await user_collection.find_one({"_id": user_id})
        if log["status"] == 1:
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            yesterday_str = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )

            new_streak = user.get("streak", 0)

            if user.get("last_completed") == today_str:
                pass
            elif user.get("last_completed") == yesterday_str:
                new_streak += 1
            else:
                new_streak = 1

            if (
                new_streak != user.get("streak")
                or user.get("last_completed") != today_str
            ):
                await user_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"streak": new_streak, "last_completed": today_str}},
                )
    updated_habit = await habits_collection.find_one({"_id": ObjectId(habit_id)})
    # updated_habit["_id"] = str(updated_habit["_id"])
    updated_workspace = await workspace_collection.find_one({"_id": workspace["_id"]})
    return {
        "message": "Logged",
        "completion_count": updated_habit["completion_count"],
        "skip_count": updated_habit["skip_count"],
        "workspace_streak": updated_workspace["streak", 0],
    }


async def get_habit_logs(habit_id: str) -> List[dict]:
    logs = []
    async for log in habits_logs_collection.find({"habit_id": ObjectId(habit_id)}):
        logs.append(log)
    return logs
