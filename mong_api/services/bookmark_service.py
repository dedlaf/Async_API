from bson import ObjectId
from fastapi import Depends, HTTPException

from db.mongo import get_mongo_db
from services.mongo_service import MongoCRUD


class BookmarkService(MongoCRUD):

    async def add_bookmark(self, user_id: str, movie_id: str):
        user = await self._get_user(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if movie_id not in user["bookmarks"]:
            user["bookmarks"].append(movie_id)
            await self.update_document(
                collection_name="User",
                condition={"_id": ObjectId(user_id)},
                new_values=user,
            )
        else:
            raise HTTPException(status_code=400, detail="Bookmark already exists")
        return user

    async def delete_bookmark(self, user_id: str, movie_id: str):
        user = await self._get_user(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if movie_id in user["bookmarks"]:
            user["bookmarks"].remove(movie_id)
            await self.update_document(
                collection_name="User",
                condition={"_id": ObjectId(user_id)},
                new_values=user,
            )
        else:
            raise HTTPException(status_code=404, detail="Bookmark not found")
        return user

    async def get_bookmarks(self, user_id: str):
        user = await self._get_user(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user["bookmarks"]

    async def _get_user(self, user_id: ObjectId):
        return await self.find(collection_name="User", condition={"_id": user_id})


def get_bookmark_service(mongo=Depends(get_mongo_db)):
    return BookmarkService(db=mongo)
