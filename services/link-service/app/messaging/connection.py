import aio_pika
from loguru import logger

from app.core.config import settings


async def get_connection() -> aio_pika.abc.AbstractRobustConnection:
    logger.info("Connecting to RabbitMQ", extra={"host": settings.rabbitmq_host})
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    logger.info("Connected to RabbitMQ")

    return connection
