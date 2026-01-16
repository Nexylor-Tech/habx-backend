from datetime import datetime, timezone
from typing import List

from bson import ObjectId

from app.db import tasks_collection


async def get_tasks(ws_id: str) -> List[dict]:
    tasks = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    async for task in tasks_collection.find({"workspace_id": ObjectId(ws_id)}):
        is_overdue = 0
        if task["deadline"] and task["status"] != 1:
            if task["deadline"] < today:
                is_overdue = 1
        task["overdue"] = is_overdue
        tasks.append({**task, "is_overdue": is_overdue})
    return tasks


async def create_task(task: dict, workspace_id: str):
    today = datetime.now(timezone.utc)
    is_overdue = 0
    if task["deadline"] and task["deadline"] < today:
        is_overdue = 1
    new_task = {
        "workspace_id": ObjectId(workspace_id),
        "title": task["title"],
        "deadline": task["deadline"],
        "status": 0,
        "is_overdue": is_overdue,
    }
    result = await tasks_collection.insert_one(new_task)
    return await tasks_collection.find_one({"_id": result.inserted_id})


async def update_task(task_id: str, update) -> dict:
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if update_data:
        await tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data},
        )
    return {"message": "Task updated successfully"}


# async def delete_task(task_id: ObjectId, user_id: ObjectId) -> None:
#     await tasks_collection.delete_one({"_id": task_id, "user_id": user_id})
