from logging import config as logging_config

import backoff
from pika.exceptions import AMQPError
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    name: str = Field(default="EPK Service")

    debug: bool = False
    enable_tracer: bool = False

    authjwt_secret_key: str = Field(default="movies_token_secret")
    authjwt_algorithm: str = Field(default="HS256")

    model_config = SettingsConfigDict(extra="ignore")


# Класс настройки Kafka
class RabbitMQSettings(BaseSettings):
    username: str = Field(alias="RABBITMQ_DEFAULT_USER")
    password: str = Field(alias="RABBITMQ_DEFAULT_PASS")
    host: str = Field(default="rabbitmq")
    port: str = Field(default="5672")
    exchange: str = Field(default="")
    virtual_host: str = Field(default="/")
    message_ttl: int = Field(default=86400000)

    model_config = SettingsConfigDict(env_prefix="rabbitmq_", extra="ignore")

    def get_dsn(self):
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}{self.virtual_host}"

    @staticmethod
    def get_backoff_settings():
        """
        Получение настроек для backoff
        """
        return {
            'wait_gen': backoff.expo,
            'exception': AMQPError,
            'logger': 'rmq_publisher',
            'base': 2,
            'factor': 1,
            'max_value': 60
        }


class GunicornSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=2)
    loglevel: str = Field(default="debug")
    model_config = SettingsConfigDict(env_prefix="gunicorn_", extra="ignore")


settings = Settings()
gunicorn_settings = GunicornSettings()
rabbitmq_settings = RabbitMQSettings()
