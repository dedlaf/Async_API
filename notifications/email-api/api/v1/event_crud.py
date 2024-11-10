import uuid

from fastapi import APIRouter, Depends, HTTPException

from db.postgres import get_db_connection
from schemas.shemas import EventCreate

router = APIRouter()


@router.post("/")
async def create_event(event_data: EventCreate, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        event_id = str(uuid.uuid4())
        insert_query = "INSERT INTO notify.event (id, template_id, content_id, users, timestamp, created, modified) VALUES (%s, %s, %s, %s::uuid[], %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"

        cursor.execute(
            insert_query,
            (
                event_id,
                event_data.template_id,
                event_data.content_id,
                event_data.users,
                event_data.timestamp,
            ),
        )

        postgres.commit()
        cursor.close()
        return {"message": "Event created", "event_id": event_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании события: {e}")


@router.get("/{event_id}")
async def get_event(event_id: str, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        select_query = "SELECT id, template_id, content_id, users, timestamp, created, modified FROM notify.event WHERE id = %s"
        cursor.execute(select_query, (event_id,))
        result = cursor.fetchone()

        if result:
            event_data = {
                "id": result[0],
                "template_id": result[1],
                "content_id": result[2],
                "users": result[3],
                "timestamp": result[4],
                "created": result[5],
                "modified": result[6],
            }
            cursor.close()
            return event_data
        else:
            raise HTTPException(status_code=404, detail="Event not found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении события: {e}"
        )

    finally:
        cursor.close()


@router.put("/{event_id}")
async def update_event(
    event_id: str, event_data: EventCreate, postgres=Depends(get_db_connection)
):
    try:
        cursor = postgres.cursor()
        update_query = "UPDATE notify.event SET template_id = %s, content_id = %s, users = %s::uuid[], timestamp = %s, modified = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(
            update_query,
            (
                event_data.template_id,
                event_data.content_id,
                event_data.users,
                event_data.timestamp,
                event_id,
            ),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found")

        postgres.commit()
        cursor.close()
        return {"message": f"Event with ID {event_id} updated"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении события: {e}"
        )


@router.delete("/{event_id}")
async def delete_event(event_id: str, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        delete_query = "DELETE FROM notify.event WHERE id = %s"
        cursor.execute(delete_query, (event_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found")

        postgres.commit()
        cursor.close()
        return {"message": f"Event with ID {event_id} deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении события: {e}")


@router.get("/")
async def get_all_events(postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        select_query = "SELECT id, template_id, content_id, users, timestamp, created, modified FROM notify.event"
        cursor.execute(select_query)
        results = cursor.fetchall()

        events = []
        for row in results:
            events.append(
                {
                    "id": row[0],
                    "template_id": row[1],
                    "content_id": row[2],
                    "users": row[3],
                    "timestamp": row[4],
                    "created": row[5],
                    "modified": row[6],
                }
            )

        cursor.close()
        return events

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении событий: {e}"
        )
