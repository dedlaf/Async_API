from enum import Enum


class StorageKey(Enum):
    LAST_MODIFIED_FILMWORK = "last_modified_filmwork"
    LAST_MODIFIED_GENRE = "last_modified_genre"


class TableName(Enum):
    FILM_WORK = "film_work"
    GENRE = "genre"
    PERSON = "person"
