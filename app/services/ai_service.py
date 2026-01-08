import json
from datetime import date, datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException
from google import genai

from app.config import settings
from app.db import analytics_cache, habits_collection, habits_logs_collection

client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())


def generate_habits(goal: str):
    if not settings.GEMINI_API_KEY.get_secret_value():
        raise HTTPException(status_code=500, detail="Gemini API key not found")
    prompt = f'''
    You are an expert habit coach, behavioral psychologist, and wellness guide.

    A user’s primary goal is:
    "{goal}"

    Your task is to generate exactly 20 DAILY habits that strongly and directly support this goal.

    STRICT REQUIREMENTS (DO NOT IGNORE):
    1. Every habit must be:
       - Small and realistic (5–30 minutes OR a clearly measurable quantity)
       - Actionable and concrete (NO vague wording)
       - Easy to complete daily

    2. Each habit MUST include:
       - A specific number, duration, or count
         (e.g. "drink 3 liters of water", "walk 7,000 steps", "meditate for 8 minutes")
       - A clear action that can be tracked as done/not done

    3. The habits must be distributed across these categories:
       - Physical / Practical (fitness, health, productivity)
       - Mental focus / discipline
       - Spiritual or inner growth that is closely related to the goal
         (e.g. mindfulness, gratitude, intention-setting, self-awareness)
       Spiritual habits should feel supportive, grounded, and practical — NOT abstract or religious.

    4. Every habit must clearly relate back to the user's goal.
       If a habit does not support the goal, do NOT include it.

    5. Avoid generic phrases such as:
       - "drink more water"
       - "exercise regularly"
       - "be mindful"
       - "stay positive"
       Replace them with precise actions.

    OUTPUT FORMAT:
    Return ONLY a valid JSON array.
    No markdown.
    No explanations.

    Each object must have exactly these fields:
    - "title": short habit name (2–6 words)
    - "category": one of ["Health", "Fitness", "Wellness", "Learning", "Productivity", "Spiritual"]
    - "icon": one of ["water", "walk", "body", "brain", "mind", "sleep", "food", "listen", "write", "activity"]

    EXAMPLE QUALITY (do NOT reuse):
    - "Drink 3 liters of water"
    - "Stretch hips for 10 minutes"
    - "Write one intention sentence"
    - "Walk 7,000 steps outdoors"
    - "Meditate with breath for 6 minutes"
    '''
    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed generation: {str(e)}")


async def generate_analytics(user_id: dict) -> dict:
    cache_data = await analytics_cache.find_one(
        {"user_id": user_id["_id"], "type": "ai_insight"}
    )

    if cache_data:
        created_at = cache_data.get("created_at")
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if created_at and (datetime.now(timezone.utc) - created_at).days < 1:
            return cache_data.get("data")

    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    has_logs = await habits_logs_collection.find_one(
        {"user_id": user_id["_id"], "date": yesterday}
    )

    if not has_logs:
        return {"insight": "No data available", "tips": ["Finish some tasks"]}

    habits = []
    async for h in habits_collection.find({"user_id": user_id["_id"]}):
        habits.append(
            {
                "title": h["title"],
                "completed": h["completion_count"],
                "skipped": h["skip_count"],
            }
        )

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
        res = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )
        text = res.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        await analytics_cache.update_one(
            {"user_id": user_id["_id"]},
            {
                "$set": {
                    "created_at": datetime.now(timezone.utc),
                    "data": data,
                    "type": "ai_insight",
                }
            },
            upsert=True,
        )

        return data
    except Exception as e:
        print(f"Error generating AI insight: {e}")
        return {
            "insight": "Keep traking ur progress",
            "tips": ["Reveiew ur goals daily"],
        }


async def generate_insight_weekly(user_id: dict) -> List[dict]:
    today = datetime.now(timezone.utc).date()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    pipeline = [
        {"$match": {"user_id": user_id["_id"], "date": {"$in": dates}}},
        {
            "$group": {
                "_id": "$date",
                "completed": {"$sum": {"$cond": [{"$eq": ["$status", 1]}, 1, 0]}},
                "skipped": {"$sum": {"$cond": [{"$eq": ["$status", 0]}, 1, 0]}},
            }
        },
    ]

    results = await habits_logs_collection.aggregate(pipeline)
    results_list = await results.to_list(length=1)
    data_map = {
        item["_id"]: {"completed": item["completed"], "skipped": item["skipped"]}
        for item in results_list
    }
    stats = []
    for d in dates:
        entry = data_map.get(d, {"completed": 0, "skipped": 0})
        stats.append(
            {"date": d, "completed": entry["completed"], "skipped": entry["skipped"]}
        )
        print(entry)
    return stats
