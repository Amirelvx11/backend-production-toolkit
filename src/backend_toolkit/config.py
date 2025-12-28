import os
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "backend-toolkit"
    environment: str = Field(default="local")
    debug: bool = False

    log_level: str = "INFO"
    log_json: bool = True

    # Mongo Logging
    mongo_log_enabled: bool = False
    mongo_uri: str | None = None
    mongo_db: str = "logs"
    mongo_collection: str = "app_logs"

    model_config = SettingsConfigDict(
        env_prefix="BT_",
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
