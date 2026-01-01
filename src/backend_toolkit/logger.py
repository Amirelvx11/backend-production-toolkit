import logging
import sys
import json
from .config import settings
from .utils.timezone import now_iran_str

try:
    from backend_toolkit.mongo_handler import MongoLogHandler
except Exception:
    MongoLogHandler = None


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": now_iran_str(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": settings.app_name,
            "environment": settings.environment,
        }
        if hasattr(record, "run_id"):
            payload["run_id"] = record.run_id
        return json.dumps(payload)


class IranFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return now_iran_str()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)

    stream_handler = logging.StreamHandler(sys.stdout)

    if settings.log_json:
        stream_handler.setFormatter(JsonFormatter())
    else:
        stream_handler.setFormatter(
            IranFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

    logger.addHandler(stream_handler)

    # Mongo Handler
    if (
        getattr(settings, "mongo_log_enabled", False)
        and getattr(settings, "mongo_uri", None)
        and MongoLogHandler is not None
    ):
        try:
            logger.addHandler(MongoLogHandler())
        except Exception:
            # Never crash app because of logging
            pass

    logger.propagate = False
    return logger
