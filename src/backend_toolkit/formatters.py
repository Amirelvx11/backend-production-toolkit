import json
import logging
import traceback
from backend_toolkit.config import settings
from backend_toolkit.utils.timezone import now_iran_str


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
        "taskName",
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


class TextFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        )
