import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    project_name: str = "email-api"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_login: str
    rabbitmq_password: str

    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_database: str

settings = Settings(_env_file=".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
