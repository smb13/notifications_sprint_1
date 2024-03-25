from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


async def get_producer() -> AIOKafkaProducer:
    return producer
