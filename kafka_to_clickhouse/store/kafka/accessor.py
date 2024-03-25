from typing import Any, List, Union

from confluent_kafka import Consumer
from store.base import BaseAccessor

from core.config import settings
from core.logger import logger

configure_consumer = {
    "bootstrap.servers": settings.kafka.bootstrap_servers,
    "group.id": "service_events",
    "auto.offset.reset": "earliest",
    "enable_auto_commit": False,
}


class KafkaAccessor(BaseAccessor):
    def __init__(self) -> None:
        self.consumer: Consumer = Consumer(configure_consumer)
        self.__subscribe(settings.kafka.topic_subscribe)

    def __subscribe(self, topic: List[str]) -> None:
        self.consumer.subscribe(topic)

    def __enter__(self) -> Union[Consumer, Exception]:
        try:
            return self.consumer
        except ConnectionError as c_e:
            logger.warning("Connection in Kafka is not available. %s", repr(c_e))
            raise

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.consumer.close()
