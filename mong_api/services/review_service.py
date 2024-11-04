from datetime import datetime

from bson import ObjectId
from fastapi import Depends, HTTPException

from db.mongo import get_mongo_db
from services.mongo_service import MongoCRUD


class ReviewService(MongoCRUD):

    async def add_review(
        self, user_id: str, movie_id: str, text: str, author: str, user_rating: int
    ):
        user_rating = self._normalize_rating(user_rating)
        review = self._create_review(user_id, movie_id, text, author, user_rating)
        review["_id"] = await self.insert_document(
            collection_name="Review", data=review
        )
        return review

    async def update_review(self, review_id: str, text: str, user_rating: int):
        user_rating = self._normalize_rating(user_rating)
        if not (review := await self.get_review(review_id)):
            raise HTTPException(status_code=404, detail="Review not found")
        self._update_review(review, text, user_rating)
        await self.update_document(
            collection_name="Review",
            condition={"_id": ObjectId(review_id)},
            new_values=review,
        )
        return review

    async def delete_review(self, review_id: str):
        if not await self.get_review(review_id):
            raise HTTPException(status_code=404, detail="Review not found")
        await self.delete_document(
            collection_name="Review", condition={"_id": ObjectId(review_id)}
        )
        return {"status": "Review deleted"}

    async def get_review(self, review_id: str):
        return await self.find(
            collection_name="Review", condition={"_id": ObjectId(review_id)}
        )

    def _create_review(
        self, user_id: str, movie_id: str, text: str, author: str, user_rating: int
    ):
        return {
            "user_id": user_id,
            "movie_id": movie_id,
            "text": text,
            "publication_date": datetime.utcnow(),
            "author": author,
            "user_rating": user_rating,
            "likes": 0,
            "dislikes": 0,
        }

    def _update_review(self, review: dict, text: str, user_rating: int):
        review["text"] = text
        review["user_rating"] = user_rating

    def _normalize_rating(self, rating: int) -> int:
        return min(max(0, rating), 10)


def get_review_service(mongo=Depends(get_mongo_db)):
    return ReviewService(db=mongo)
