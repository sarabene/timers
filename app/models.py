import uuid
import datetime
from pydantic import BaseModel, Field, HttpUrl

class Timer(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    webhook_url: HttpUrl
    timestamp: datetime.datetime

class TimerRequest(BaseModel):
    '''
    Pydantic model representing the request body for creating a timer.
    Enforces validation rules:
    - hours, minutes, seconds must be greater than or equal to 0
    - hours, minutes, seconds must be integers
    - webhook_url must be a valid URL
    '''
    hours: int = Field(ge=0)
    minutes: int = Field(ge=0)
    seconds: int = Field(ge=0)
    webhook_url: HttpUrl
