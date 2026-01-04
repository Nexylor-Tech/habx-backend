from pydantic import BaseModel


class HabitLogCreate(BaseModel):
    date: str
    status: int


class WeeklyStats(BaseModel):
    date: str
    count: int


class LogResponse(BaseModel):
    date: str
    status: int
