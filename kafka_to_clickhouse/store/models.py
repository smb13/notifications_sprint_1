import datetime as dt
import json
import uuid
from typing import Any, Dict, Optional

from pydantic import BaseModel, field_serializer


class Event(BaseModel):
    user_id: Optional[str]
    timestamp: dt.datetime
    value: Optional[Dict[str, Any]]

    @field_serializer("value")
    def serialize_value(self, value: Dict[str, Any]) -> str:
        return json.dumps(value)

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: dt.datetime) -> int:
        return int(timestamp.timestamp())


class User(Event):
    pass


class Film(Event):
    film_id: uuid.UUID

    @field_serializer("film_id")
    def serialize_film_id(self, film_id: uuid.UUID) -> str:
        return str(film_id)
