from fastapi import APIRouter, Depends, HTTPException
from schemas.shemas import ContentCreate, ContentUpdate
from services.content_service import ContentService, get_content_service

router = APIRouter()


@router.get("/")
async def get_all_contents(
    content_service: ContentService = Depends(get_content_service),
):
    return content_service.get_all_contents()


@router.post("/")
async def create_content(
    content_data: ContentCreate,
    content_service: ContentService = Depends(get_content_service),
):
    content_service.create_content(content_data)
    return {"message": "Content created"}


@router.get("/content/{content_id}")
async def get_content(
    content_id: str, content_service: ContentService = Depends(get_content_service)
):
    content = content_service.get_content(content_id)
    if content:
        return content
    raise HTTPException(status_code=404, detail="Content not found")


@router.put("/{content_id}")
async def update_content(
    content_id: str,
    content_data: ContentUpdate,
    content_service: ContentService = Depends(get_content_service),
):
    result = content_service.update_content(content_id, content_data)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": f"Content with ID {content_id} updated"}


@router.delete("/{content_id}")
async def delete_content(
    content_id: str, content_service: ContentService = Depends(get_content_service)
):
    result = content_service.delete_content(content_id)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": f"Content with ID {content_id} deleted"}
