from pydantic import BaseModel, Field
from typing import Optional

class HabitCreate(BaseModel):
    title: str
    category: str
    icon: Optional[str] = "activity"

class HabitUpdate(BaseModel):
    completion_count: int
    skip_count: int

class HabitResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    category: str
    icon: str
    completion_count: int
    skip_count: int