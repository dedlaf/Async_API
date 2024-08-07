import logging
import uuid
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from services.person import PersonService, get_person_service

router = APIRouter()


class PersonResponse(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    full_name: str
    films: Optional[List[dict]] = []


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
    request: Request,
    query: str = "",
    page: int = 0,
    page_size: int = 50,
    person_service: PersonService = Depends(get_person_service),
) -> List[PersonResponse]:
    logging.info(query)
    offset_min = page * page_size
    offset_max = (page + 1) * page_size
    persons = await person_service.get_list(request=str(request.url), query=query)
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

    return final_data[offset_min:offset_max]


@router.get("/{person_id}/film", response_model=list)
async def person_details_film(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> List[dict]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person.films
