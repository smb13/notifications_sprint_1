import backoff
from proccess.exctract import KafkaExtractor
from proccess.load import ClickhouseLoader
from proccess.transform import DataTransform
from store.clickhouse.accessor import ClickhouseAccessor
from store.kafka.accessor import KafkaAccessor

from core.config import settings
from core.logger import logger


@backoff.on_exception(backoff.expo, Exception, logger=logger, max_tries=settings.project.backoff_max_tries)
def main() -> None:
    logger.info("Start ETL process...")
    with ClickhouseAccessor() as click, KafkaAccessor() as kafka_consumer:
        load = ClickhouseLoader().run(click)
        transform = DataTransform().run(next_node=load)
        extract = KafkaExtractor().run(next_node=transform)

        while True:
            messages = kafka_consumer.consume(num_messages=settings.project.batch_size, timeout=1.0)
            if messages:
                extract.send((kafka_consumer, settings.kafka.topic_subscribe, messages))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("User terminated the process")
