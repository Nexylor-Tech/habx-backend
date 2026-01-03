from typing import List

from bson import ObjectId

from app.db import habits_collection


async def get_habits(user_id: ObjectId) -> List[dict]:
    habits = []
    async for habit in habits_collection.find({"user_id": user_id}):
        habit["_id"] = str(habit["_id"])
        habits.append(habit)
    return habits


async def create_habit(habit: dict, user_id: ObjectId) -> dict:
    new_habit = {
        "user_id": user_id,
        "title": habit["title"],
        "category": habit["category"],
        "icon": habit.get("icon", "activity"),
        "completion_count": 0,
        "skip_count": 0,
    }
    result = await habits_collection.insert_one(new_habit)
    habit["_id"] = str(result.inserted_id)
    return habit


async def update_habit(
    habit_id: str, completion_count: int, skip_count: int, user_id: ObjectId
) -> None:
    await habits_collection.update_one(
        {"_id": ObjectId(habit_id), "user_id": user_id},
        {"$set": {"completion_count": completion_count, "skip_count": skip_count}},
    )
