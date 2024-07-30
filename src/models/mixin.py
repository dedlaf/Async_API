import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TimeStampedMixin(BaseModel):
    created: Optional[datetime] = None
    modified: Optional[datetime] = None


class UUIDMixin(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
