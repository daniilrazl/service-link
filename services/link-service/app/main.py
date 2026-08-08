from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api import links_router
from app.core.config import settings
from common.src.logging import setup_logging

setup_logging(level=settings.log_level, log_format=settings.log_format)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    yield
    logger.info("Application is shutting down")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(links_router)


@app.get("/health")
async def health() -> dict[str, str]:
    logger.info("Health check requested")
    return {
        "status": "ok",
        "service": settings.app_name,
    }
