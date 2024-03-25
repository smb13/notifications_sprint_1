from typing import Annotated

from annotated_types import IsNotNan, MinLen
from pydantic import BaseModel


class Message(BaseModel):
    """
    Сообщение для Kafka
    """

    # Топик
    topic: Annotated[str, IsNotNan, MinLen(1)]
    # Временная метка
    timestamp_ms: int
    # Ключ сообщения
    key: bytes
    # Значение сообщения
    value: bytes | None
