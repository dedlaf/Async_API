import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from models.film import Film
from models.person import Person
from services.film import FilmService, get_film_service

router = APIRouter()


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
    if filter:
        filters["filter"] = filter
    sort_by["sort"] = sort
    films = await film_service.get_list_of_films(
        sort=sort_by, filters=filters, query=query, request=str(request.url)
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


# TODO: Раскомментировать после готового ETL пайплайна для персоналий
# TODO: Доделать url пути для персоналий
# TODO: Написать функцию для списка персоналий
"""

@router.get('/persons/{person_id}', response_model=Person)
async def film_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
   person = await person_service.get_by_id(person_id)
   if not person:
       raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
   return Person(id=str(person.id), title=person.full_name)
   
"""
