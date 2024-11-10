import random

import pymongo
from bson.objectid import ObjectId
from faker import Faker


class DataSeeder:
    def __init__(self, _db_name, count):
        self._fake = Faker()
        self._db_name = _db_name
        self._record_count = count
        self._client = pymongo.MongoClient("mongodb://admin:Qwertys1@mongodb:27017/")
        self._db = self._client[self._db_name]
        self._user_collection = self._db["User"]
        self._review_collection = self._db["Review"]
        self._like_collection = self._db["Like"]

    @staticmethod
    def __generate_user_ratings(num_users=5):
        user_ratings = {}
        for _ in range(num_users):
            user_id = f"user{random.randint(1, 1000)}"
            rating = random.randint(1, 10)
            user_ratings[user_id] = rating
        return user_ratings

    def __generate_user_record(self):
        return {
            "_id": ObjectId(),
            "name": self._fake.name(),
            "email": self._fake.email(),
            "age": self._fake.random_int(min=18, max=80),
            "bookmarks": [self._fake.word(), self._fake.word()],
        }

    def __generate_movie_review_record(self):
        return {
            "_id": ObjectId(),
            "user_id": str(ObjectId()),
            "movie_id": str(ObjectId()),
            "text": self._fake.text(),
            "publication_date": self._fake.date_time_this_decade(),
            "author": self._fake.name(),
            "likes": self._fake.random_int(min=0, max=1000),
            "dislikes": self._fake.random_int(min=0, max=1000),
            "user_rating": self._fake.random_int(min=0, max=10),
        }

    def __generate_movie_rating_record(self):
        user_ratings = self.__generate_user_ratings()
        average_rating = round(sum(user_ratings.values()) / len(user_ratings), 1)
        return {
            "_id": ObjectId(),
            "movie_id": str(ObjectId()),
            "user_ratings": user_ratings,
            "rating": average_rating,
        }

    def __seed_movie_reviews(self):
        records = [
            self.__generate_movie_review_record() for _ in range(self._record_count)
        ]
        self._review_collection.insert_many(records)

    def __seed_movie_ratings(self):
        records = [
            self.__generate_movie_rating_record() for _ in range(self._record_count)
        ]
        self._like_collection.insert_many(records)

    def __seed_users(self):
        records = [self.__generate_user_record() for _ in range(self._record_count)]
        self._user_collection.insert_many(records)

    def _generate_all(self):
        users = [self.__generate_user_record() for _ in range(self._record_count)]
        movie_reviews = [
            self.__generate_movie_review_record() for _ in range(self._record_count)
        ]
        movie_ratings = [
            self.__generate_movie_rating_record() for _ in range(self._record_count)
        ]

        return {"User": users, "Review": movie_reviews, "Like": movie_ratings}

    def seed_all(self):
        data = self._generate_all()
        self._user_collection.insert_many(data["User"])
        self._review_collection.insert_many(data["Review"])
        self._like_collection.insert_many(data["Like"])
        return data["User"][0], data["Review"][0], data["Like"][0]

    def clear_all_collections(self):
        self._db["User"].delete_many({})
        self._db["Review"].delete_many({})
        self._db["Like"].delete_many({})


if __name__ == "__main__":
    db_name = "testdb"
    record_count = 100

    seeder = DataSeeder(_db_name=db_name, count=record_count)
    seeder.clear_all_collections()
