from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Any, Dict, List

from db.mongo import get_mongo_db


class MongoCRUD:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def insert_document(self, collection_name: str, data: dict) -> Any:
        collection = self.db[collection_name]
        res = await collection.insert_one(data)
        return res.inserted_id

    async def find(self, collection_name: str, condition: dict, multiple: bool = False):
        collection = self.db[collection_name]
        if multiple:
            results = collection.find(condition)
            return [item async for item in results]
        return await collection.find_one(condition)

    async def update_document(self, collection_name: str, condition: dict, new_values: dict):
        collection = self.db[collection_name]
        await collection.update_one(condition, {'$set': new_values})

    async def delete_document(self, collection_name: str, condition: dict):
        collection = self.db[collection_name]
        result = await collection.delete_one(condition)
        return result

def get_mongo_crud(mongo=Depends(get_mongo_db)):
    return MongoCRUD(db=mongo)
