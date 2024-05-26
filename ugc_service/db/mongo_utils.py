from core.config import settings
from db.get_mongo import db
from motor.motor_asyncio import AsyncIOMotorClient


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(str(settings.MONGODB_URL))


async def close_mongo_connection():
    db.client.close()
