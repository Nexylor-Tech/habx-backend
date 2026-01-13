from typing import Dict, List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class WorkspaceCreate(BaseModel):
    name: str
    goal: str
    initial_habits: List[Dict[str, str]] = []


class WorkspaceResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    goal: str
