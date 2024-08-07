import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from models.genre import Genre
from services.genres import GenreService, get_genre_service

router = APIRouter()

@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Genre(
        id=genre.id,
        name=genre.name,
        description=genre.description,
    )


@router.get("/", response_model=List[Genre])
async def genre_list(request: Request, genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    genres = await genre_service.get_list_of_genres(request=str(request.url))
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    final_data = [
        Genre(
            id=genre.id,
            name=genre.name,
            description=genre.description,
        )
        for genre in genres
    ]

    return final_data