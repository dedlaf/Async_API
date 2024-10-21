from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    bootstrap_servers: str
    clickhouse_host: str = "clickhouse"
    batch_size: int = 1000
