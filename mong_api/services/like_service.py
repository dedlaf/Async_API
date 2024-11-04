from bson import ObjectId
from fastapi import Depends, HTTPException

from db.mongo import get_mongo_db
from services.mongo_service import MongoCRUD


class LikeService(MongoCRUD):

    async def add_rating(self, movie_id: str, user_id: str, user_rating: int):
        user_rating = self._normalize_rating(user_rating)
        like = await self._get_like(movie_id)
        if like:
            self._update_like(like, user_id, user_rating)
            await self.update_document(
                collection_name="Like",
                condition={"movie_id": movie_id},
                new_values=like,
            )
        else:
            like = self._create_like(movie_id, user_id, user_rating)
            like["_id"] = await self.insert_document(collection_name="Like", data=like)
        return like

    async def update_rating(self, movie_id: str, user_id: str, user_rating: int):
        user_rating = self._normalize_rating(user_rating)
        if not (like := await self._get_like(movie_id)):
            raise HTTPException(status_code=404, detail="Like not found")
        if user_id not in like["user_ratings"]:
            raise HTTPException(
                status_code=404, detail="User rating not found in movie"
            )
        self._update_like(like, user_id, user_rating)
        await self.update_document(
            collection_name="Like", condition={"movie_id": movie_id}, new_values=like
        )
        return like

    async def delete_rating(self, movie_id: str, user_id: str):
        if not (like := await self._get_like(movie_id)):
            raise HTTPException(status_code=404, detail="Like not found")
        self._remove_rating(like, user_id)
        (
            await self.update_document(
                collection_name="Like",
                condition={"movie_id": movie_id},
                new_values=like,
            )
            if like["user_ratings"]
            else await self.delete_document(
                collection_name="Like", condition={"movie_id": movie_id}
            )
        )
        return {"status": "Like deleted"}

    async def _get_like(self, movie_id: str):
        return await self.find(
            collection_name="Like", condition={"_id": ObjectId(movie_id)}
        )

    def _update_like(self, like: dict, user_id: str, user_rating: int):
        like["user_ratings"][user_id] = user_rating
        self._recalculate_rating(like)

    def _remove_rating(self, like: dict, user_id: str):
        if user_id in like["user_ratings"]:
            del like["user_ratings"][user_id]
            self._recalculate_rating(like) if like["user_ratings"] else None
        else:
            raise HTTPException(
                status_code=404, detail="User rating not found in movie"
            )

    @staticmethod
    def _create_like(movie_id: str, user_id: str, user_rating: int):
        return {
            "movie_id": movie_id,
            "user_ratings": {user_id: user_rating},
            "rating": round(user_rating, 1),
        }

    @staticmethod
    def _recalculate_rating(like: dict):
        total_ratings = sum(like["user_ratings"].values())
        like["rating"] = round(
            max(0, min(total_ratings / len(like["user_ratings"]), 10)), 1
        )

    @staticmethod
    def _normalize_rating(rating: int) -> int:
        return min(max(0, rating), 10)


def get_like_service(mongo=Depends(get_mongo_db)):
    return LikeService(db=mongo)
