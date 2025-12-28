from pydantic import BaseModel
from datetime import datetime

class BaseEvent(BaseModel):
    run_id: str
    created_at: datetime
