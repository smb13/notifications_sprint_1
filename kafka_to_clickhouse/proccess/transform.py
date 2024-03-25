from collections.abc import Generator
from typing import Any, List, Tuple, Dict

from pydantic import TypeAdapter
from store import models

from core.logger import logger
from utils.decorator import get_value_from_generator


class DataTransform:
    @get_value_from_generator
    def run(self, next_node: Generator) -> Generator[None, List[Tuple[str, Dict[Any, Any]]], None]:
        while data_batch := (yield):  # type: ignore
            transformed_batch = []
            for topic, value in data_batch:
                logger.info("Data transformation before loading")
                get_class_model = getattr(models, topic.title())
                model_adapter = TypeAdapter(get_class_model)
                model_data = model_adapter.validate_python(value)
                transformed_batch.append((topic.lower(), model_data))
            next_node.send(transformed_batch)
