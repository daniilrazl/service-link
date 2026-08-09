import aio_pika
from loguru import logger


async def get_connection(url: str) -> aio_pika.abc.AbstractRobustConnection:
    logger.info("Connecting to RabbitMQ")
    connection = await aio_pika.connect_robust(url)
    logger.info("Connected to RabbitMQ")

    return connection
