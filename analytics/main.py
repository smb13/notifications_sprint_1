import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from aiokafka import AIOKafkaProducer
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.v1 import events, health_check
from core.config import kafka_settings, project_settings
from core.logger import LOGGING
from db import kafka


@asynccontextmanager
async def lifespan(_: FastAPI) -> Any:
    # Создаем подключение к базам при старте сервера.
    kafka.producer = AIOKafkaProducer(bootstrap_servers=kafka_settings.connection_string)

    # Соединяемся с кластером Kafka
    await kafka.producer.start()

    yield

    # Отключаемся от кластера Kafka
    await kafka.producer.stop()


@AuthJWT.load_config
def get_config() -> object:
    return project_settings


app = FastAPI(
    # Название проекта, используемое в документации.
    title=project_settings.name,
    # Адрес документации (swagger).
    docs_url="/analytics/openapi",
    # Адрес документации (openapi).
    openapi_url="/analytics/openapi.json",
    # Оптимизация работы с JSON-сериализатором.
    default_response_class=ORJSONResponse,
    # Указываем функцию, обработки жизненного цикла приложения.
    lifespan=lifespan,
    # Описание сервиса
    description="API информации о ",
)

# Подключаем роутер к серверу с указанием префикса для API
app.include_router(events.router, prefix="/analytics/v1")
app.include_router(health_check.router, prefix="/health_check/v1")


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    # Запускаем приложение с помощью uvicorn сервера.
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
