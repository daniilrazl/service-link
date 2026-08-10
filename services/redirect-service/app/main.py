from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api import redirect_router
from app.core.config import settings
from app.core.database import async_session_maker
from app.messaging import LinkCreatedConsumer
from app.services import redirect_service
from common.src.logging import setup_logging
from common.src.messaging import EventPublisher, get_connection

setup_logging(level=settings.log_level, log_format=settings.log_format)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    connection = await get_connection(settings.rabbitmq_url)
    publisher = EventPublisher(connection, settings.rabbitmq_exchange_name)
    await publisher.setup()
    redirect_service.init_publisher(publisher)

    consumer = LinkCreatedConsumer(async_session_maker)
    await consumer.setup()
    await consumer.start()

    yield

    logger.info("Application shutting down...")
    await consumer.close()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(redirect_router, prefix="/r")


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }
