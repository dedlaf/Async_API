from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}

    PROJECT_NAME: str = "auth"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int


class User(BaseModel):
    username: str = "test"
    password: str = "test"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
PROJECT_NAME = settings.PROJECT_NAME

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
