from typing import Dict, Optional

from pydantic import BaseModel, Field


class LikeSchema(BaseModel):
    movie_id: str = Field(..., description="ID фильма")
    user_ratings: Dict[str, int] = Field(
        ..., description="Оценки пользователей в формате user_id: рейтинг"
    )
    rating: Optional[float] = Field(None, description="Средняя оценка фильма")


class LikeInDB(LikeSchema):
    id: str = Field(..., description="ID в базе данных")


class LikeInput(BaseModel):
    movie_id: str
    user_id: str
    rating: int


class LikeDeleteInput(BaseModel):
    movie_id: str
    user_id: str
