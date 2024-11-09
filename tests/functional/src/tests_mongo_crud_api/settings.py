import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="..env")

    mongodb_uri: str = "mongodb://admin:Qwertys1@mongodb:27017"


settings = Settings(_env_file="..env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
