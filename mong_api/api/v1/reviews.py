from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas.review import ReviewInDB, ReviewInput, ReviewUpdateInput
from services.review_service import ReviewService, get_review_service

router = APIRouter()


@router.post(
    "/",
    response_model=ReviewInDB,
    summary="Добавление новой рецензии",
    description="Добавляет новую рецензию в базу данных",
)
async def create_review(
    review_input: ReviewInput,
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        review = await review_service.add_review(
            review_input.user_id,
            review_input.movie_id,
            review_input.text,
            review_input.author,
            review_input.user_rating,
        )
        return ReviewInDB(id=str(review["_id"]), **review)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/{review_id}",
    response_model=ReviewInDB,
    summary="Получение рецензии по идентификатору",
    description="Возвращает данные рецензии по её id",
)
async def get_review(
    review_id: str, review_service: ReviewService = Depends(get_review_service)
):
    review = await review_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review["id"] = str(review.pop("_id"))
    return review


@router.put(
    "/{review_id}",
    response_model=ReviewInDB,
    summary="Обновление данных рецензии",
    description="Обновляет данные рецензии по её id и возвращает обновлённую рецензию",
)
async def update_review(
    review_id: str,
    review_input: ReviewUpdateInput,
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        review = await review_service.update_review(
            review_id, review_input.text, review_input.user_rating
        )
        return ReviewInDB(id=str(review["_id"]), **review)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete(
    "/{review_id}",
    response_model=dict,
    summary="Удаление рецензии",
    description="Удаляет рецензию по её id",
)
async def delete_review(
    review_id: str, review_service: ReviewService = Depends(get_review_service)
):
    try:
        result = await review_service.delete_review(review_id)
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/",
    response_model=List[ReviewInDB],
    summary="Получение списка рецензий",
    description="Возвращает список всех рецензий в базе данных",
)
async def get_reviews(review_service: ReviewService = Depends(get_review_service)):
    reviews = await review_service.find(
        collection_name="Review", condition={}, multiple=True
    )
    for review in reviews:
        review["id"] = str(review.pop("_id"))
    return reviews
