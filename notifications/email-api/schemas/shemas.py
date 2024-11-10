from datetime import datetime

from pydantic import BaseModel


class TemplateUpdate(BaseModel):
    new_template: str
    new_template_name: str


class ContentCreate(BaseModel):
    words: dict


class ContentUpdate(BaseModel):
    words: dict


class EventCreate(BaseModel):
    template_id: str
    content_id: str
    users: list[str]
    timestamp: datetime
