import json
from collections.abc import Generator
from typing import Any, Tuple, Dict

import backoff
from confluent_kafka import Consumer

from core.config import settings
from core.logger import logger
from utils.decorator import get_value_from_generator


class KafkaExtractor:
    @get_value_from_generator
    @backoff.on_exception(backoff.expo, Exception, logger=logger, max_tries=settings.project.backoff_max_tries)
    def run(self, next_node: Generator) -> Generator[None, Tuple[Consumer, str, Dict[Any, Any]], None]:
        messages_batch = []

        while True:
            consumer, topics, batch_data = yield

            for message in batch_data:
                if message.error():
                    logger.error(f"Response error {message.error()} ({message.error().code()}) from kafka service")
                    continue

                topic = message.topic()
                if topic not in topics:
                    continue

                logger.info(f"Received message from topic {topic}")

                user_id = message.key().decode("utf-8")
                value = json.loads(message.value().decode("utf-8"))
                film_id = value.pop("film_id", None)

                event_data = {
                    "user_id": user_id,
                    "timestamp": message.timestamp()[1],
                    "value": value,
                }

                if film_id:
                    event_data = {**event_data, "film_id": film_id}

                messages_batch.append((topic, event_data))

                if len(messages_batch) >= settings.project.batch_size:
                    next_node.send(messages_batch)
                    consumer.commit()
                    messages_batch = []
