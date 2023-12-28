from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)


def get_db():
    return client.get_database("smart-learning-workspace")
