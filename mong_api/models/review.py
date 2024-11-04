from datetime import datetime

from beanie import Document


class Review(Document):
    user_id: str
    movie_id: str
    text: str
    publication_date: datetime
    author: str
    likes: int = 0
    dislikes: int = 0
    user_rating: int
