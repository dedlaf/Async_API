from fastapi import APIRouter, Depends, HTTPException
from schemas.shemas import TemplateUpdate
from services.template_service import TemplateService, get_template_service

router = APIRouter()


@router.get("/")
async def get_all_templates(
    template_service: TemplateService = Depends(get_template_service),
):
    return template_service.get_all_templates()


@router.get("/{template_id}")
async def get_template(
    template_id: str, template_service: TemplateService = Depends(get_template_service)
):
    template = template_service.get_template(template_id)
    if template:
        return template
    raise HTTPException(status_code=404, detail="Template not found")


@router.post("/")
async def create_template(
    template_name: str,
    template_body: str,
    template_service: TemplateService = Depends(get_template_service),
):
    template_service.create_template(template_name, template_body)
    return {"message": "Template created"}


@router.put("/{template_id}")
async def update_template(
    template_id: str,
    template_data: TemplateUpdate,
    template_service: TemplateService = Depends(get_template_service),
):
    result = template_service.update_template(template_id, template_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": f"Template with ID {template_id} updated"}


@router.delete("/{template_id}")
async def delete_template(
    template_id: str, template_service: TemplateService = Depends(get_template_service)
):
    result = template_service.delete_template(template_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": f"Template with ID {template_id} deleted"}
