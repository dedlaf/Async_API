from pydantic import BaseModel


class Message(BaseModel):
    topic: str
    key: str
    value: str
