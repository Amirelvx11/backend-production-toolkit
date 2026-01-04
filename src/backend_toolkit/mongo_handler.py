import logging
from pymongo import MongoClient
from .config import settings
from .logger import JsonFormatter
from .utils.timezone import now_iran_str

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
    
    def __init__(self):
        super().__init__()
        client = get_mongo_client()
        self.collection = client[settings.mongo_db][settings.mongo_collection]

    def emit(self, record: logging.LogRecord):
        try:
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

            self.collection.insert_one(log_doc)
        except Exception as exc:
            logging.getLogger(__name__).debug(
                "MongoLogHandler emit failed",
                exc_info=exc,
            )
            pass
