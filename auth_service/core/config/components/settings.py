import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}

    project_name: str = "auth"

    redis_host: str = "redis"
    redis_port: int = 6379

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    yandex_client_id: str
    yandex_client_secret: str

    vk_client_id: str
    vk_client_secret: str
    vk_code_verifier: str
    vk_redirect_uri: str

    enable_tracer: bool = False


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
