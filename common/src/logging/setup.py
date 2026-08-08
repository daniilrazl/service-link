import logging
import sys

from loguru import logger

from common.src.logging.formatter import json_formatter, text_formatter
from common.src.logging.handler import InterceptHandler


def setup_logging(level: str = "INFO", log_format: str = "text") -> None:
    logger.remove()

    formatter = json_formatter if log_format.lower() == "json" else text_formatter

    def sink(message) -> None:
        record = message.record
        output = formatter(record)
        sys.stdout.write(output)
        sys.stdout.flush()

    logger.add(
        sink,
        level=level.upper(),
        colorize=False,
    )

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(0)

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True