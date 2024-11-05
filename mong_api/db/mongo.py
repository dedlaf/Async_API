from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

mongodb = None


async def get_mongo_db() -> AsyncIOMotorDatabase:
    if mongodb is None:
        raise ValueError("MongoDB is not initialized")
    return mongodb
