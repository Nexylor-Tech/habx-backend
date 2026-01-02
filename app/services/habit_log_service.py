from bson.objectid import ObjectId

from app.db import habits_collection, habits_logs_collection


async def log_habit(habit_id: str, log: dict, user_id: ObjectId):
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
