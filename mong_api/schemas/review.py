from datetime import datetime

from pydantic import BaseModel, Field


class ReviewInput(BaseModel):
    user_id: str = Field(..., description="ID пользователя")
    movie_id: str = Field(..., description="ID фильма")
    text: str = Field(..., description="Текст рецензии")
    author: str = Field(..., description="Автор рецензии")
    user_rating: int = Field(..., description="Оценка фильма пользователем")


class ReviewUpdateInput(BaseModel):
    text: str = Field(..., description="Текст рецензии")
    user_rating: int = Field(..., description="Оценка фильма пользователем")


class ReviewInDB(BaseModel):
    id: str = Field(..., description="ID рецензии в базе данных")
    user_id: str = Field(..., description="ID пользователя")
    movie_id: str = Field(..., description="ID фильма")
    text: str = Field(..., description="Текст рецензии")
    publication_date: datetime = Field(..., description="Дата публикации рецензии")
    author: str = Field(..., description="Автор рецензии")
    user_rating: int = Field(..., description="Оценка фильма пользователем")
    likes: int = Field(0, description="Количество лайков")
    dislikes: int = Field(0, description="Количество дизлайков")
