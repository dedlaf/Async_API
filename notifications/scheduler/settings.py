from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_database: str

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str

    class Config:
        env_file = ".env"


config = DatabaseConfig()
print(config.db_database, config.db_host, config.db_port)