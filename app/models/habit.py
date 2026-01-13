from typing import Optional

from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class HabitCreate(BaseModel):
    title: str
    category: str
    icon: Optional[str] = "activity"


class HabitUpdate(BaseModel):
    completion_count: int
    skip_count: int


class HabitResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    category: str
    icon: str
    completion_count: int
    skip_count: int
