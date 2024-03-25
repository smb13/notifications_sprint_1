import json
from functools import lru_cache
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException

from db.kafka import get_producer
from models.message import Message
from schemas.event import CreateEventResponse, UserEvent


class EventService:
    """
    EventService содержит бизнес-логику по работе с пользовательскими событиями.
    """

    def __init__(self, producer: AIOKafkaProducer, jwt: AuthJWT) -> None:
        self.producer = producer
        self.jwt = jwt

    async def create_event(self, action_name: str, event_create: UserEvent) -> CreateEventResponse:
        message = await self._get_kafka_message(action_name=action_name, event=event_create)
        try:
            await self.producer.send_and_wait(**message.model_dump())
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error send message to Kafka: {e}",
            )
        return CreateEventResponse(event_sent=True)

    async def _get_kafka_message(self, action_name: str, event: UserEvent) -> Message:
        value_dict = {"action": action_name}
        if event.film_id:
            topic = "film"
            value_dict.update({"film_id": event.film_id})
        else:
            topic = "user"
        if event.value:
            value_dict.update(event.value)
        value = json.dumps(value_dict).encode("utf-8")

        key = (await self.jwt.get_raw_jwt())["sub"]

        return Message(topic=topic, timestamp_ms=event.timestamp, key=key, value=value)


@lru_cache
def get_event_service(
    producer: AIOKafkaProducer = Depends(get_producer),
    jwt: AuthJWT = Depends(),
) -> EventService:
    return EventService(producer, jwt)
