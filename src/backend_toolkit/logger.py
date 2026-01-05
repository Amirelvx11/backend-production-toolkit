import logging
import sys
from backend_toolkit.config import settings
from backend_toolkit.mongo_handler import MongoLogHandler
from backend_toolkit.formatters import JsonFormatter, TextFormatter


def resolve_log_level(level: str) -> int:
    level = level.upper()
    if level not in logging._nameToLevel:
        raise ValueError(f"Invalid log level: {level}")
    return logging._nameToLevel[level]


LOG_LEVEL = resolve_log_level(settings.log_level)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(LOG_LEVEL)

        sh.setFormatter(
            JsonFormatter() if settings.log_json else TextFormatter()
        )
        logger.addHandler(sh)

    if settings.mongo_log_enabled and settings.mongo_uri:
        if not any(isinstance(h, MongoLogHandler) for h in logger.handlers):
            logger.addHandler(MongoLogHandler())

    return logger
