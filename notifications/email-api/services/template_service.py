import uuid

from core.queries import TemplateQueries
from fastapi import Depends, HTTPException
from schemas.shemas import TemplateUpdate
from services.query_service import get_query_service


class TemplateService:
    def __init__(self, query_service):
        self.query_service = query_service

    def get_all_templates(self):
        try:
            results = self.query_service.fetch_all(TemplateQueries.SELECT_ALL)
            templates = [
                {
                    "id": row[0],
                    "template_name": row[1],
                    "template": row[2],
                    "created": row[3],
                    "modified": row[4],
                }
                for row in results
            ]
            return templates
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении шаблонов: {e}"
            )

    def get_template(self, template_id: str):
        try:
            result = self.query_service.fetch_one(
                TemplateQueries.SELECT_BY_ID, (template_id,)
            )
            if result:
                return {
                    "id": result[0],
                    "template_name": result[1],
                    "template": result[2],
                    "created": result[3],
                    "modified": result[4],
                }

            return None
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при получении шаблона: {e}"
            )

    def create_template(self, template_name: str, template_body: str):
        try:
            uuid_id = uuid.uuid4()
            self.query_service.execute_query(
                TemplateQueries.CREATE, (str(uuid_id), template_name, template_body)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при создании шаблона: {e}"
            )

    def update_template(self, template_id: str, template_data: TemplateUpdate):
        try:
            if self.get_template(template_id) is None:
                return None
            self.query_service.execute_query(
                TemplateQueries.UPDATE,
                (
                    template_data.new_template_name,
                    template_data.new_template,
                    template_id,
                ),
            )
            return "Updated"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при обновлении шаблона: {e}"
            )

    def delete_template(self, template_id: str):
        try:
            if self.get_template(template_id) is None:
                return None
            self.query_service.execute_query(TemplateQueries.DELETE, (template_id,))
            return "Deleted"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка при удалении шаблона: {e}"
            )


def get_template_service(query_service=Depends(get_query_service)):
    return TemplateService(query_service)
