from typing import Optional

from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class TaskCreate(BaseModel):
    title: str
    deadline: Optional[str] = ""


class TaskUpdate(BaseModel):
    status: int = Field(default=0)


class TaskResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    deadline: Optional[str] = None
    status: int = Field(default=0)
    is_overdue: Optional[int] = Field(default=0)
