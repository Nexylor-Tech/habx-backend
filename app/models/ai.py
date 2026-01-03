from typing import List

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    goal: str


class SuggestionResponse(BaseModel):
    title: str
    category: str
    icon: str


class AnalyticsResponse(BaseModel):
    insight: str
    tips: List[str]


class WeeklyAnalyticsResponse(BaseModel):
    date: str
    count: int
