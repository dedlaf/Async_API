from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    email: str = Field(..., description="Email пользователя")
    age: int = Field(..., description="Возраст пользователя")
    bookmarks: List[str] = Field(
        [], description="Список ID фильмов, добавленных в закладки"
    )


class UserInDB(User):
    id: str = Field(..., description="ID в базе данных")
