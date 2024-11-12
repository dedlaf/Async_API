import json
import uuid

from core.queries import ContentQueries
from fastapi import Depends, HTTPException
from schemas.shemas import ContentCreate, ContentUpdate
from services.query_service import get_query_service


class ContentService:
    def __init__(self, query_service):
        self.query_service = query_service

    def get_all_contents(self):
        try:
            results = self.query_service.fetch_all(ContentQueries.SELECT_ALL)
            contents = [
                {"id": row[0], "words": row[1], "created": row[2], "modified": row[3]}
                for row in results
            ]
            return contents
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении контента: {e}"
            )

    def get_content(self, content_id: str):
        try:
            result = self.query_service.fetch_one(
                ContentQueries.SELECT_BY_ID, (content_id,)
            )
            if result:
                return {
                    "id": result[0],
                    "words": result[1],
                    "created": result[2],
                    "modified": result[3],
                }
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении контента: {e}"
            )

    def create_content(self, content_data: ContentCreate):
        try:
            content_id = str(uuid.uuid4())
            words_json = json.dumps(content_data.words)
            self.query_service.execute_query(
                ContentQueries.CREATE, (content_id, words_json)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при создании контента: {e}"
            )

    def update_content(self, content_id: str, content_data: ContentUpdate):
        try:
            if self.get_content(content_id) is None:
                return None
            words_json = json.dumps(content_data.words)
            self.query_service.execute_query(
                ContentQueries.UPDATE, (words_json, content_id)
            )
            return "Updated"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при обновлении контента: {e}"
            )

    def delete_content(self, content_id: str):
        try:
            if self.get_content(content_id) is None:
                return None
            self.query_service.execute_query(ContentQueries.DELETE, (content_id,))
            return "Deleted"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении контента: {e}"
            )


def get_content_service(query_service=Depends(get_query_service)):
    return ContentService(query_service)
