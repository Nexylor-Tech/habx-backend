from datetime import datetime, timedelta, timezone
from typing import List

from bson.objectid import ObjectId

from app.db import habits_collection, habits_logs_collection, user_collection


async def log_habit(
    habit_id: str, log: dict, user_id: ObjectId, last_completed: str, streak: int
):
    print(user_id)
    print(type(user_id))
    print(isinstance(user_id, dict))
    await habits_logs_collection.update_one(
        {"user_id": user_id, "habit_id": ObjectId(habit_id), "date": log["date"]},
        {"$set": {"status": log["status"]}},
        upsert=True,
    )
    field_to_inc = "completion_count" if log["status"] == 1 else "skip_count"

    await habits_collection.update_one(
        {"_id": ObjectId(habit_id), "user_id": user_id},
        {"$inc": {field_to_inc: 1}},
    )

    # user = await user_collection.find_one({"_id": user_id})
    if log["status"] == 1:
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        yesterday_str = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )

        new_streak = streak

        if last_completed == today_str:
            pass
        elif last_completed == yesterday_str:
            new_streak += 1
        else:
            new_streak = 1

        if new_streak != streak or last_completed != today_str:
            await user_collection.update_one(
                {"_id": user_id},
                {"$set": {"streak": new_streak, "last_completed": today_str}},
            )


async def get_habit_logs(habit_id: str, user_id: dict) -> List[dict]:
    logs = []
    async for log in habits_logs_collection.find(
        {"habit_id": ObjectId(habit_id), "user_id": user_id}
    ):
        print(f"habit_id: {habit_id}, user_id: {user_id}")
        logs.append(log)
    return logs
