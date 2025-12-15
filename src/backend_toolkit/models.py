from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class LogRecord:
    timestamp: datetime
    level: str
    service: str
    message: str
    context: dict[str, Any] | None = None
