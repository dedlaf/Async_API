import json
import uuid

from db.postgres import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from schemas.shemas import ContentCreate, ContentUpdate

router = APIRouter()


@router.get("/")
async def get_all_contents(postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        select_query = "SELECT id, words, created, modified FROM notify.content"
        cursor.execute(select_query)
        results = cursor.fetchall()

        contents = []
        for row in results:
            contents.append(
                {"id": row[0], "words": row[1], "created": row[2], "modified": row[3]}
            )

        cursor.close()
        return contents

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении контента: {e}"
        )


@router.post("/")
async def create_content(
    content_data: ContentCreate, postgres=Depends(get_db_connection)
):
    try:
        cursor = postgres.cursor()
        content_id = str(uuid.uuid4())
        words_json = json.dumps(content_data.words)
        insert_query = "INSERT INTO notify.content (id, words, created, modified) VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
        cursor.execute(insert_query, (content_id, words_json))

        postgres.commit()
        cursor.close()
        return {"message": "Content created", "content_id": content_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при создании контента: {e}"
        )


@router.get("/{content_id}")
async def get_content(content_id: str, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        select_query = (
            "SELECT id, words, created, modified FROM notify.content WHERE id = %s"
        )
        cursor.execute(select_query, (content_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            content_data = {
                "id": result[0],
                "words": result[1],
                "created": result[2],
                "modified": result[3],
            }
            return content_data
        else:
            raise HTTPException(status_code=404, detail="Content not found")

    except Exception as e:
        cursor.close()
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении контента: {e}"
        )


@router.put("/{content_id}")
async def update_content(
    content_id: str, content_data: ContentUpdate, postgres=Depends(get_db_connection)
):
    try:
        cursor = postgres.cursor()
        words_json = json.dumps(content_data.words)
        update_query = "UPDATE notify.content SET words = %s, modified = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(update_query, (words_json, content_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Content not found")

        postgres.commit()
        cursor.close()
        return {"message": f"Content with ID {content_id} updated"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении контента: {e}"
        )


@router.delete("/{content_id}")
async def delete_content(content_id: str, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        delete_query = "DELETE FROM notify.content WHERE id = %s"
        cursor.execute(delete_query, (content_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Content not found")
        postgres.commit()
        cursor.close()
        return {"message": f"Content with ID {content_id} deleted"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при удалении контента: {e}"
        )
