from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "link-service"
    debug: bool = False

    short_code_length: int = 8

    postgres_user: str = "user"
    postgres_password: SecretStr = SecretStr("pass")
    postgres_host: str = "host"
    postgres_port: int = 1
    postgres_db: str = "link_db"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    rabbitmq_user: str = "user"
    rabbitmq_password: SecretStr = SecretStr("pass")
    rabbitmq_host: str = "host"
    rabbitmq_port: int = 1

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password.get_secret_value()}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    log_level: str = "INFO"
    log_format: str = "text"


settings = Settings()
