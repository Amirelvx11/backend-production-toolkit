import logging
from datetime import datetime

from .config import settings
from .models import LogRecord


class BaseLogger:
    def __init__(self, service_name: str | None = None):
        self.service_name = service_name or settings.SERVICE_NAME
        self._logger = logging.getLogger(self.service_name)
        self._logger.setLevel(settings.LOG_LEVEL)

    def info(self, message: str, context: dict | None = None):
        self._emit("INFO", message, context)

    def error(self, message: str, context: dict | None = None):
        self._emit("ERROR", message, context)

    def _emit(self, level: str, message: str, context: dict | None):
        record = LogRecord(
            timestamp=datetime.utcnow(),
            level=level,
            service=self.service_name,
            message=message,
            context=context,
        )

        # For now: stdout (later Mongo, Kafka, etc.)
        self._logger.log(
            getattr(logging, level),
            f"{record.timestamp.isoformat()} | {record.level} | {record.service} | {record.message} | {record.context}"
        )
