import json

import aio_pika
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.repositories import LinkRepository
from common.src.messaging import LinkCreated, get_connection
from common.src.messaging.constants import EXCHANGE_TYPE, ROUTING_KEY_LINK_CREATED


class LinkCreatedConsumer:
    QUEUE_NAME = "redirect-service.link-created"

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._repo = LinkRepository()
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._queue: aio_pika.abc.AbstractQueue | None = None

    async def setup(self) -> None:
        self._connection = await get_connection(settings.rabbitmq_url)
        self._channel = await self._connection.channel()

        exchange = await self._channel.declare_exchange(
            settings.rabbitmq_exchange_name,
            EXCHANGE_TYPE,
            durable=True,
        )

        self._queue = await self._channel.declare_queue(
            self.QUEUE_NAME,
            durable=True,
        )

        await self._queue.bind(exchange, routing_key=ROUTING_KEY_LINK_CREATED)

        logger.info(
            "Consumer setup complete",
            extra={"queue": self.QUEUE_NAME, "exchange": settings.rabbitmq_exchange_name},
        )

    async def start(self) -> None:
        if self._queue is None:
            raise RuntimeError("Consumer not initialized. Call setup() first")

        logger.info("Consumer started", extra={"queue": self.QUEUE_NAME})
        await self._queue.consume(self._handle_message)

    async def _handle_message(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                event = LinkCreated(**body)

                logger.info(
                    "Received LinkCreated event",
                    extra={"short_code": event.short_code},
                )

                async with self._session_factory() as session:
                    existing = await self._repo.get_by_short_code(session, event.short_code)
                    if existing:
                        logger.warning(
                            "Link already exists, skipping",
                            extra={"short_code": event.short_code},
                        )

                        return

                    await self._repo.create(
                        session,
                        short_code=event.short_code,
                        original_url=event.original_url,
                    )
                    await session.commit()

                    logger.info(
                        "Link saved for redirect",
                        extra={"short_code": event.short_code},
                    )
            except Exception as e:
                logger.error(
                    "Failed to process LinkCreated event",
                    extra={"error": str(e), "body": message.body.decode()},
                )

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()
            logger.info("Consumer connection closed")
