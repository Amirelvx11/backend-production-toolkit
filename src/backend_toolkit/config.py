import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ENV: str = os.getenv("ENV", "local")
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "backend-toolkit")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Mongo logging (optional for now)
    MONGO_URI: str | None = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB", "logs")

settings = Settings()
