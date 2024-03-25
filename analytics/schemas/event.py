import time as tm

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Dict


def get_now_in_ms() -> int:
    return round(tm.time() * 1000)


class UserEvent(BaseModel):
    """
    Пользовательское событие
    """

    timestamp: int = Field(
        ...,
        default_factory=get_now_in_ms,
        description="Метка времени события в ms",
        examples=[1708767326343],
    )
    film_id: str | None = Field(
        None,
        description="Идентификатор фильма",
        examples=["3d825f60-9fff-4dfe-b294-1a45fa1e115d"],
    )
    value: Dict[str, str] | None = Field(
        None,
        description="Метаданные пользовательского события в формате Dict[str, str]",
        examples=[{"view_uri": "/films/favourites", "view_duration": "4561"}],
    )

    model_config = ConfigDict(from_attributes=True)


class CreateEventResponse(BaseModel):
    """
    Ответ на создание события
    """

    event_sent: bool = Field(
        ...,
        description="Сообщение отправлено в кластер Kafka",
        examples=[True],
    )

    model_config = ConfigDict(from_attributes=True)


class HealthCheckResponse(BaseModel):
    """
    Статус работы
    """

    status: str
