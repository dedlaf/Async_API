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
