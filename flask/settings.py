from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    kafka_host: str
    sentry_sdk: str
    logstash_host: str


settings = Settings()
kafka_host = settings.kafka_host
sentrysdk = settings.sentry_sdk
