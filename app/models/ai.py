from pydantic import BaseModel

class GenerateRequest(BaseModel):
    goal: str

class SuggestionResponse(BaseModel):
    title: str
    category: str
    icon: str