from pydantic import BaseModel
import uuid


class KafkaData(BaseModel):
    user_id: uuid.UUID
    topic: str
    value: str
