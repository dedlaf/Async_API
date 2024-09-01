from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Settings(BaseModel):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}

    PROJECT_NAME: str = "auth"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int


class User(BaseModel):
    username: str = "test"
    password: str = "test"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

DSL = {
    "dbname": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
    "host": settings.db_host,
    "port": settings.db_port,
}

PROJECT_NAME = settings.PROJECT_NAME

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

