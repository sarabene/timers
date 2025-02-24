import uuid
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class Timer(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    webhook_url: HttpUrl
    timestamp: datetime
    is_executed: bool = False

class TimerRequest(BaseModel):
    hours: int
    minutes: int
    seconds: int
    webhook_url: HttpUrl
