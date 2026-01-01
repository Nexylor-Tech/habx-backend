import json
from typing import List

from fastapi import HTTPException
from google import genai

from app.config import settings
from app.db import habits_collection, user_collection

client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())


def generate_habits(goal: str):
    if not settings.GEMINI_API_KEY.get_secret_value():
        raise HTTPException(status_code=500, detail="Gemini API key not found")
    prompt = f'''
    Generate 20 small, daily, actionable habits for a user whose main goal is: "{goal}".

    Return the response as a valid JSON array of objects. Each object must have:
    - "title": A short habit name (2-5 words).
    - "category": One of [Health, Learning, Fitness, Wellness, Social, Productivity, Finance].
    - "icon": One of [water, book, activity, mind, food, sleep, write, code, walk, phone, home, off, money, plan, body, pill, brain, listen, face].

    Do not include markdown formatting like ```json. Just return the raw JSON array.
    '''
    try:
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed generation: {str(e)}")


async def generate_analytics(user_id: dict) -> List[dict]:
    print(user_id)
    if not settings.GEMINI_API_KEY.get_secret_value():
        raise HTTPException(status_code=500, detail="Gemini API key not found")

    habits = []
    async for h in habits_collection.find({"user_id": user_id["_id"]}):
        habits.append(
            {
                "title": h["title"],
                "completed": h["completion_count"],
                "skipped": h["skip_count"],
            }
        )
    print(habits)
    prompt = f"""
    The user has a main goal: "{user_id.get("goal")}".
    Here is their habit performance data: {json.dumps(habits)}.

    Based on this data, generate:
    1. A short, encouraging paragraph summarizing their progress (key "insight").
    2. A list of 3 specific actionable tips to improve (key "tips").

    Return as a valid JSON object with keys "insight" and "tips".
    Do not include markdown formatting.
    """
    try:
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Failed to generate insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed generation: {str(e)}")
