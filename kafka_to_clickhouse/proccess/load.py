from collections import defaultdict
from collections.abc import Generator
from typing import TypeVar, List, Tuple, Dict, Any

import backoff
from store import models
from store.clickhouse.accessor import ClickhouseAccessor

from core.config import settings
from core.logger import logger
from utils.decorator import get_value_from_generator

ModelsSchemas = TypeVar("ModelsSchemas", bound=models)


class ClickhouseLoader:
    @get_value_from_generator
    @backoff.on_exception(backoff.expo, Exception, logger=logger, max_tries=settings.project.backoff_max_tries)
    def run(self, click: ClickhouseAccessor) -> Generator[None, List[Tuple[str, ModelsSchemas]], None]:
        while data_batch := (yield):  # type: ignore
            write_batches = defaultdict(List)

            for table_name, model_data in data_batch:

                logger.info(f"Saving in table {table_name}")

                # Prepare batch data for saving
                dict_data_for_saving: Dict[str, Any] = model_data.model_dump()

                fields = ", ".join(dict_data_for_saving.keys())

                write_batches[(table_name, fields)].append(dict_data_for_saving)

            for (table_name, fields), values in write_batches.items():
                query = f"INSERT INTO {table_name} ({fields}) VALUES"
                logger.debug(f"Batch data for saving {query=}")

                click.cursor.execute(query, values)
