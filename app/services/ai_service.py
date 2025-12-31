import json
from google import genai
from fastapi import HTTPException
from app.config import settings

def generate_habits(goal: str):
    if not settings.GEMINI_API_KEY.get_secret_value():
        raise HTTPException(status_code=500, detail="Gemini API key not found")
    client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())
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