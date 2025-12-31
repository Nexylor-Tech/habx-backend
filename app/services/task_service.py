from typing import List

from bson import ObjectId

from app.db import tasks_collection


async def get_tasks(user_id: ObjectId) -> List[dict]:
    tasks = []
    async for task in tasks_collection.find({"user_id": user_id}):
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks


async def create_task(task: dict, user_id: ObjectId) -> dict:
    new_task = {
        "user_id": user_id,
        "title": task["title"],
        "deadline": task["deadline"],
        "completed": False,
    }
    result = await tasks_collection.insert_one(new_task)
    task["_id"] = str(result.inserted_id)
    return task


async def update_task(task_id: ObjectId, completed: bool, user_id: ObjectId) -> None:
    await tasks_collection.update_one(
        {"_id": ObjectId(task_id), "user_id": user_id},
        {"$set": {"completed": completed}},
    )


# async def delete_task(task_id: ObjectId, user_id: ObjectId) -> None:
#     await tasks_collection.delete_one({"_id": task_id, "user_id": user_id})
