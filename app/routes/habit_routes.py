from typing import List

from fastapi import APIRouter, Depends

from app.deps import auth
from app.models.habit import HabitCreate, HabitResponse, HabitUpdate
from app.models.habit_log import HabitLogCreate
from app.services import habit_log_service, habit_service

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("/", response_model=List[HabitResponse])
async def get_habits(current_user: dict = Depends(auth.get_current_user)):
    return await habit_service.get_habits(current_user["_id"])


@router.post("/")
async def create_habit(
    habit: HabitCreate, current_user: dict = Depends(auth.get_current_user)
):
    return await habit_service.create_habit(habit.model_dump(), current_user["_id"])


@router.post("/{habit_id}/log")
async def log_habit(
    habit_id: str,
    log: HabitLogCreate,
    current_user: dict = Depends(auth.get_current_user),
):
    return await habit_log_service.log_habit(
        habit_id, log.model_dump(), current_user["_id"]
    )


@router.patch("/{habit_id}")
async def update_habit(
    habit_id: str,
    update: HabitUpdate,
    current_user: dict = Depends(auth.get_current_user),
):
    return await habit_service.update_habit(
        habit_id, update.completion_count, update.skip_count, current_user["_id"]
    )
