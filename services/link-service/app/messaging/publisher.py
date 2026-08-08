import json

import aio_pika
from loguru import logger

from app.core.config import settings
from app.messaging.constants import (
    DELIVERY_MODE,
    EXCHANGE_TYPE,
)
from app.messaging.events import Event


class EventPublisher:
    def __init__(self, connection: aio_pika.abc.AbstractRobustConnection):
        self.connection = connection
        self.exchange: aio_pika.abc.AbstractExchange | None = None

    async def setup(self) -> None:
        channel = await self.connection.channel()
        self.exchange = await channel.declare_exchange(
            settings.rabbitmq_exchange_name,
            EXCHANGE_TYPE,
            durable=True,
        )

        logger.info("Exchange declared", extra={"exchange": settings.rabbitmq_exchange_name})

    async def publish(self, event: Event) -> None:
        if self.exchange is None:
            raise RuntimeError("Publisher not initialized. Call setup() first.")

        message = aio_pika.Message(
            body=json.dumps(event.to_dict()).encode(),
            content_type="application/json",
            delivery_mode=DELIVERY_MODE,
        )

        await self.exchange.publish(message, routing_key=event.routing_key)

        logger.info(
            "Event published",
            extra={
                "event_type": type(event).__name__,
                "routing_key": event.routing_key,
            },
        )
