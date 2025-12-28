import logging
import sys
import json
from datetime import datetime
from backend_toolkit.config import settings
from backend_toolkit.mongo_handler import MongoLogHandler

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "run_id"):
            payload["run_id"] = record.run_id
        return json.dumps(payload)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)

    stream_handler  = logging.StreamHandler(sys.stdout)
    
    if settings.log_json:
        stream_handler.setFormatter(JsonFormatter())
    else:
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

    logger.addHandler(stream_handler)
    
    # Mongo Handler
    if settings.mongo_log_enabled and settings.mongo_uri:
        mongo_handler = MongoLogHandler()
        logger.addHandler(mongo_handler)  
    
    logger.propagate = False
    return logger
