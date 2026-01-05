import logging
from pymongo import MongoClient
from backend_toolkit.config import settings
from backend_toolkit.formatters import JsonFormatter
from backend_toolkit.utils.timezone import now_iran_str

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            settings.mongo_uri,
            tz_aware=True,
            connectTimeoutMS=3000,
            serverSelectionTimeoutMS=3000,
        )
    return _client


class MongoLogHandler(logging.Handler):
    RESERVED = JsonFormatter.RESERVED

    def emit(self, record: logging.LogRecord):
        try:
            client = get_mongo_client()
            collection = client[settings.mongo_db][settings.mongo_collection]

            log_doc = {
                "timestamp": now_iran_str(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "environment": settings.environment,
                "app": settings.app_name,
            }

            for key, value in record.__dict__.items():
                if key not in self.RESERVED and key not in log_doc:
                    log_doc[key] = value

            collection.insert_one(log_doc)

        except Exception:
            logging.getLogger("mongo-logger").error(
                "MongoLogHandler emit failed",
                exc_info=True,
            )
