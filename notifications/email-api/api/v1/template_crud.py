import http
import uuid

from db.postgres import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from schemas.shemas import TemplateUpdate

router = APIRouter()


@router.get("/")
async def get_all_templates(postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        select_query = (
            "SELECT id, template_name, template, created, modified FROM notify.template"
        )
        cursor.execute(select_query)
        results = cursor.fetchall()

        templates = []
        for row in results:
            templates.append(
                {
                    "id": row[0],
                    "template_name": row[1],
                    "template": row[2],
                    "created": row[3],
                    "modified": row[4],
                }
            )

        cursor.close()
        return templates

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении шаблонов: {e}"
        )


@router.get("/{id}")
async def get_template(template_id: str, postgres=Depends(get_db_connection)):
    cursor = postgres.cursor()
    select_query = "SELECT id, template, template_name, created, modified FROM notify.template WHERE id = %s"
    cursor.execute(select_query, (template_id,))
    result = cursor.fetchone()
    if result:
        template_data = {
            "id": result[0],
            "template": result[1],
            "template_name": result[2],
            "created": result[3],
            "modified": result[4],
        }
        return template_data
    return http.HTTPStatus.NOT_FOUND


@router.post("/")
async def create_template(
    template_name: str, template_body: str, postgres=Depends(get_db_connection)
):
    uuid_id = uuid.uuid4()
    query = (
        f"INSERT INTO notify.template (id, template_name, template, created, modified) "
        f"VALUES ('{str(uuid_id)}', '{str(template_name)}', '{str(template_body)}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);"
    )
    cursor = postgres.cursor()
    cursor.execute(query)
    postgres.commit()
    cursor.close()
    return {"message": "Template created"}


@router.put("/{template_id}")
async def update_template(
    template_id: str, template_data: TemplateUpdate, postgres=Depends(get_db_connection)
):
    query = "UPDATE notify.template SET template_name = %s, template = %s, modified = CURRENT_TIMESTAMP WHERE id = %s"
    cursor = postgres.cursor()
    cursor.execute(
        query,
        (template_data.new_template_name, template_data.new_template, template_id),
    )
    postgres.commit()
    cursor.close()
    return {"message": f"Template with ID {template_id} updated"}


@router.delete("/{template_id}")
async def delete_template(template_id: str, postgres=Depends(get_db_connection)):
    try:
        cursor = postgres.cursor()
        delete_query = "DELETE FROM notify.template WHERE id = %s"
        cursor.execute(delete_query, (template_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Template not found")
        postgres.commit()
        cursor.close()
        return {"message": f"Template with ID {template_id} deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении шаблона: {e}")
