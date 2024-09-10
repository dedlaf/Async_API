from pydantic import BaseModel


class UserLoginHistoryResponseSchema(BaseModel):
    date: list[str]
