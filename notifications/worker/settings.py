from pydantic_settings import BaseSettings


class RbmqConfig(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str

    smtp_server: str = "smtp.mail.ru"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    from_email: str

    class Config:
        env_file = ".env"


settings = RbmqConfig()
