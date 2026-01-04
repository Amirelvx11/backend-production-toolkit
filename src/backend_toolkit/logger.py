import logging
import sys
import json
import traceback
from .config import settings
from .utils.timezone import now_iran_str

try:
    from backend_toolkit.mongo_handler import MongoLogHandler
except Exception:
    MongoLogHandler = None


class JsonFormatter(logging.Formatter):
    RESERVED = {
        "name", "msg", "args", "levelname", "levelno",
        "pathname", "filename", "module",
        "exc_info", "exc_text", "stack_info",
        "lineno", "funcName", "created",
        "msecs", "relativeCreated",
        "thread", "threadName",
        "processName", "process",
        "message", "asctime",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": now_iran_str(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": settings.app_name,
            "environment": settings.environment,
        }

        for key, value in record.__dict__.items():
            if key not in self.RESERVED and key not in payload:
                payload[key] = value        

        if record.exc_info:
            payload["exception"] = traceback.format_exception(*record.exc_info)
                
        return json.dumps(payload, default=str)        



class IranFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return now_iran_str()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level = logging._nameToLevel.get(settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

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
        settings.mongo_log_enabled
        and settings.mongo_uri
        and MongoLogHandler is not None
        and not any(isinstance(h, MongoLogHandler) for h in logger.handlers)
    ):
        try:
            logger.addHandler(MongoLogHandler())
        except Exception:
            # Never crash app because of logging
            pass

    logger.propagate = False
    return logger
