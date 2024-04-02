from collections.abc import Generator
from typing import Dict, List

import backoff

from core.config import rabbitmq_settings
from core.logger import logger
from process.decorator import coroutine
from process.load import ModelsSchemas

consuming_messages = []


class RabbitMQExtractor:
    @coroutine
    @backoff.on_exception(**rabbitmq_settings.get_backoff_settings())
    def run(self, next_node: Generator) -> Generator[
        None,
        List[Dict[str, str | ModelsSchemas]],
        None
    ]:
        while True:
            messages = yield

            logger.info(f"{len(messages)} messages was consumed from RabbitMQ and was send to transformation ...")
            next_node.send(messages)


