import uuid

from core.queries import EventQueries
from fastapi import Depends, HTTPException
from schemas.shemas import EventCreate
from services.query_service import get_query_service


class EventService:
    def __init__(self, query_service):
        self.db = query_service

    def create_event(self, event_data: EventCreate):
        try:
            event_id = str(uuid.uuid4())
            self.db.execute_query(
                EventQueries.CREATE,
                (
                    event_id,
                    event_data.template_id,
                    event_data.content_id,
                    event_data.users,
                    event_data.timestamp,
                ),
            )
            return event_id
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при создании события: {e}"
            )

    def get_event(self, event_id: str):
        try:
            result = self.db.fetch_one(EventQueries.SELECT_BY_ID, (event_id,))
            if result:
                return {
                    "id": result[0],
                    "template_id": result[1],
                    "content_id": result[2],
                    "users": result[3],
                    "timestamp": result[4],
                    "created": result[5],
                    "modified": result[6],
                }
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении события: {e}"
            )

    def update_event(self, event_id: str, event_data: EventCreate):
        try:
            if self.get_event(event_id) is None:
                return None
            self.db.execute_query(
                EventQueries.UPDATE,
                (
                    event_data.template_id,
                    event_data.content_id,
                    event_data.users,
                    event_data.timestamp,
                    event_id,
                ),
            )
            return "Updated"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при обновлении события: {e}"
            )

    def delete_event(self, event_id: str):
        try:
            if self.get_event(event_id) is None:
                return None
            self.db.execute_query(EventQueries.DELETE, (event_id,))
            return "Deleted"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении события: {e}"
            )

    def get_all_events(self):
        try:
            results = self.db.fetch_all(EventQueries.SELECT_ALL)
            events = [
                {
                    "id": row[0],
                    "template_id": row[1],
                    "content_id": row[2],
                    "users": row[3],
                    "timestamp": row[4],
                    "created": row[5],
                    "modified": row[6],
                }
                for row in results
            ]
            return events
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении событий: {e}"
            )


def get_event_service(query_service=Depends(get_query_service)):
    return EventService(query_service)
