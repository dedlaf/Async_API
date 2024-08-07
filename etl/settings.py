from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    file_path: str
    elastic_host: str
    chunk_size: int


settings = Settings()

DSL = {
    "dbname": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
    "host": settings.db_host,
    "port": settings.db_port,
}

FILE_PATH = settings.file_path
ELASTIC_HOST = settings.elastic_host
CHUNK_SIZE = settings.chunk_size
