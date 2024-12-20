from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request

from core.config.components.common_params import CommonQueryParams
from services.person import PersonService, get_person_service

from .settings import (PersonResponse, filter_query_string,
                       ignoring_request_args)

router = APIRouter()


@router.get("/{person_id}", response_model=PersonResponse)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return PersonResponse(
        id=person.id,
        full_name=person.full_name,
        films=person.films,
    )


@router.get("/search/", response_model=List[PersonResponse])
async def person_list(
    paginate: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    request: Request,
    query: str = "",
    person_service: PersonService = Depends(get_person_service),
) -> List[PersonResponse]:
    request = filter_query_string(str(request.url), ignoring_request_args)
    persons = await person_service.get_list(request=request, query=query)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    final_data = [
        PersonResponse(
            id=person.id,
            full_name=person.full_name,
            films=person.films,
        )
        for person in persons
    ]

    return final_data[paginate.offset_min : paginate.offset_max]


@router.get("/{person_id}/film", response_model=list)
async def person_details_film(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> List[dict]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person.films
