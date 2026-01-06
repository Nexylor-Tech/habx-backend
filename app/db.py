from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

from app.config import settings

client = AsyncMongoClient(
    settings.MONGO_URL.get_secret_value(), server_api=ServerApi("1")
)
if not client or client is None:
    raise ValueError("MongoDB client not initialized")

db = client.habx_db
user_collection = db.users
habits_collection = db.habits
tasks_collection = db.tasks
habits_logs_collection = db.habitslog
analytics_cache = db.analytics_cache
