import uuid
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from services.genre import GenreService, get_genre_service

router = APIRouter()


class GenreResponse(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None


@router.get("/{genre_id}", response_model=GenreResponse)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> GenreResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return GenreResponse(
        id=genre.id,
        name=genre.name,
        description=genre.description,
    )


@router.get("/", response_model=List[GenreResponse])
async def genre_list(
    request: Request, genre_service: GenreService = Depends(get_genre_service)
) -> List[GenreResponse]:
    genres = await genre_service.get_list(request=str(request.url))
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    final_data = [
        GenreResponse(
            id=genre.id,
            name=genre.name,
            description=genre.description,
        )
        for genre in genres
    ]

    return final_data
