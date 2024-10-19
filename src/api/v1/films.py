from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from core.config.components.common_params import CommonQueryParams
from core.config.components.verify_decorator import verify_user
from services.film import FilmService, get_film_service

from .settings import (FilmResponse, FilmResponseFull, filter_query_string,
                       ignoring_request_args)
import requests

router = APIRouter()



@router.get("/{film_id}", response_model=FilmResponseFull)
async def film_details(
    request: Request, film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmResponseFull:
    cookies = {
        "access_token_cookie": request.cookies.get("access_token_cookie"),
        "refresh_token_cookie": request.cookies.get("refresh_token_cookie"),
    }
    user_id = requests.get("http://auth:8070/auth/token/user", cookies=cookies).json()
    print(user_id, user_id.get("id"))
    requests.post("http://flask:5000/load-data", json={"topic": "likes", "user_id": user_id.get("id"), "value": film_id})
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return FilmResponseFull(
        id=film.id,
        title=film.title,
        description=film.description,
        creation_date=film.creation_date,
        imdb_rating=film.imdb_rating,
        genres=film.genres,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )


@router.get("/", response_model=List[FilmResponse])
@router.get("/search/", response_model=List[FilmResponse])
@verify_user
async def films_details(
    paginate: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    request: Request,
    response: Response,
    sort: str = "imdb_rating",
    filter: str = None,
    query: str = None,
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponse]:
    sort_by = {}
    filters = {}
    request = filter_query_string(str(request.url), ignoring_request_args)
    if filter:
        filters["filter"] = filter
    sort_by["sort"] = sort
    films = await film_service.get_list(
        sort=sort_by, filters=filters, query=query, request=request
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    final_data = [
        FilmResponse(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films
    ]
    if not final_data[paginate.offset_min : paginate.offset_max]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return final_data[paginate.offset_min : paginate.offset_max]
