import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    project_name: str = "email-api"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_login: str = "dedlaf"
    rabbitmq_password: str = "123qwe"


settings = Settings(_env_file=".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
