from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "movies"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    ELASTIC_HOST: str = "elasticsearch"
    ELASTIC_PORT: int = 9200


class User(BaseModel):
    username: str = "test"
    password: str = "test"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

PROJECT_NAME = settings.PROJECT_NAME

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

ELASTIC_HOST = settings.ELASTIC_HOST
ELASTIC_PORT = settings.ELASTIC_PORT
