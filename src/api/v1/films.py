import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from models.film import Film
from models.person import Person
from services.film import FilmService, get_film_service

router = APIRouter()
ignoring_request_args = ["page", "page_size"]


def filter_query_string(url, ignoring_args):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_params = {k: v for k, v in query_params.items() if k not in ignoring_args}
    filtered_query = urlencode(filtered_params, doseq=True)
    filtered_url = urlunparse(parsed_url._replace(query=filtered_query))

    return filtered_url


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        genres=film.genres,
    )


@router.get("/", response_model=List[Film])
@router.get("/search/{query}", response_model=List[Film])
async def film_details(
    request: Request,
    page: int = 0,
    page_size: int = 100,
    sort: str = "imdb_rating",
    filter: str = None,
    query: str = None,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    sort_by = {}
    filters = {}
    offset_min = page * page_size
    offset_max = (page + 1) * page_size
    request = filter_query_string(str(request.url), ignoring_request_args)
    if filter:
        filters["filter"] = filter
    sort_by["sort"] = sort
    films = await film_service.get_list_of_films(
        sort=sort_by, filters=filters, query=query, request=request
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    final_data = [
        Film(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            genres=film.genres,
        )
        for film in films
    ]
    return final_data[offset_min:offset_max]
