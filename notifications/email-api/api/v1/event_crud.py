from fastapi import APIRouter, Depends, HTTPException
from schemas.shemas import EventCreate
from services.event_service import EventService, get_event_service

router = APIRouter()


@router.post("/")
async def create_event(
    event_data: EventCreate, event_service: EventService = Depends(get_event_service)
):
    event_id = event_service.create_event(event_data)
    return {"message": "Event created", "event_id": event_id}


@router.get("/{event_id}")
async def get_event(
    event_id: str, event_service: EventService = Depends(get_event_service)
):
    event = event_service.get_event(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.put("/{event_id}")
async def update_event(
    event_id: str,
    event_data: EventCreate,
    event_service: EventService = Depends(get_event_service),
):
    result = event_service.update_event(event_id, event_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"Event with ID {event_id} updated"}


@router.delete("/{event_id}")
async def delete_event(
    event_id: str, event_service: EventService = Depends(get_event_service)
):
    result = event_service.delete_event(event_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"Event with ID {event_id} deleted"}


@router.get("/")
async def get_all_events(event_service: EventService = Depends(get_event_service)):
    return event_service.get_all_events()
