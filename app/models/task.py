from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str
    deadline: str

class TaskUpdate(BaseModel):
    completed: bool

class TaskResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    deadline: str
    completed: bool