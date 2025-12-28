import logging
from pymongo import MongoClient
from datetime import datetime
from backend_toolkit.config import settings

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
    def __init__(self):
        super().__init__()
        client = get_mongo_client()
        self.collection = client[settings.mongo_db][settings.mongo_collection]

    def emit(self, record: logging.LogRecord):
        try:
            log_doc = {
                "timestamp": datetime.utcnow(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "environment": settings.environment,
                "app": settings.app_name,
            }

            if hasattr(record, "run_id"):
                log_doc["run_id"] = record.run_id

            self.collection.insert_one(log_doc)
        except Exception:
            # prevent crashing in production
            pass
