from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from schemas.user import UserInDB
from services.bookmark_service import BookmarkService, get_bookmark_service

router = APIRouter()


class BookmarkInput(BaseModel):
    user_id: str
    movie_id: str


@router.post(
    "/",
    response_model=UserInDB,
    summary="Добавление закладки",
    description="Добавляет фильм в закладки пользователя",
)
async def add_bookmark(
    bookmark_input: BookmarkInput,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
):
    try:
        user = await bookmark_service.add_bookmark(
            bookmark_input.user_id, bookmark_input.movie_id
        )
        user["id"] = str(user.pop("_id"))
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete(
    "/",
    response_model=UserInDB,
    summary="Удаление закладки",
    description="Удаляет фильм из закладок пользователя",
)
async def delete_bookmark(
    bookmark_input: BookmarkInput,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
):
    try:
        user = await bookmark_service.delete_bookmark(
            bookmark_input.user_id, bookmark_input.movie_id
        )
        user["id"] = str(user.pop("_id"))
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get(
    "/{user_id}",
    response_model=List[str],
    summary="Получение закладок пользователя",
    description="Возвращает список всех закладок пользователя",
)
async def get_bookmarks(
    user_id: str, bookmark_service: BookmarkService = Depends(get_bookmark_service)
):
    try:
        bookmarks = await bookmark_service.get_bookmarks(user_id)
        return bookmarks
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
