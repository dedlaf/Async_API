from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from schemas.like import LikeDeleteInput, LikeInDB, LikeInput
from services.like_service import LikeService, get_like_service

router = APIRouter()


@router.post(
    "/",
    response_model=LikeInDB,
    summary="Добавление нового лайка",
    description="Добавляет новый лайк в базу данных",
)
async def create_like(
    like_input: LikeInput, like_service: LikeService = Depends(get_like_service)
):
    try:
        like = await like_service.add_rating(
            like_input.movie_id, like_input.user_id, like_input.rating
        )
        print(like)
        return LikeInDB(id=str(like["_id"]), **like)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/{like_id}",
    response_model=LikeInDB,
    summary="Получение лайка по идентификатору",
    description="Возвращает данные лайка по его id",
)
async def get_like(like_id: str, like_service: LikeService = Depends(get_like_service)):
    like = await like_service.find(
        collection_name="Like", condition={"_id": ObjectId(like_id)}
    )
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    like["id"] = str(like.pop("_id"))
    return like


@router.put(
    "/",
    response_model=LikeInDB,
    summary="Обновление данных лайка",
    description="Обновляет данные лайка по его movie_id и user_id и возвращает обновлённый лайк",
)
async def update_like(
    like_input: LikeInput, like_service: LikeService = Depends(get_like_service)
):
    try:
        like = await like_service.update_rating(
            like_input.movie_id, like_input.user_id, like_input.rating
        )
        return LikeInDB(id=str(like["_id"]), **like)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete(
    "/",
    response_model=dict,
    summary="Удаление лайка",
    description="Удаляет лайк по его movie_id и user_id",
)
async def delete_like(
    like_input: LikeDeleteInput, like_service: LikeService = Depends(get_like_service)
):
    try:
        result = await like_service.delete_rating(
            like_input.movie_id, like_input.user_id
        )
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/",
    response_model=List[LikeInDB],
    summary="Получение списка лайков",
    description="Возвращает список всех лайков в базе данных",
)
async def get_likes(like_service: LikeService = Depends(get_like_service)):
    found_likes = await like_service.find(
        collection_name="Like", condition={}, multiple=True
    )
    for like in found_likes:
        like["id"] = str(like.pop("_id"))
    return found_likes
