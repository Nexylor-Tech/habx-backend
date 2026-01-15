from typing import Dict, List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class WorkspaceCreate(BaseModel):
    name: str
    goal: Optional[str] = ""
    initial_habits: List[Dict[str, str]] = []


class WorkspaceResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    goal: str
    streak: int = 0
    last_completed: Optional[str] = None


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    # initial_habits: Optional[List[Dict[str, str]]] = None
