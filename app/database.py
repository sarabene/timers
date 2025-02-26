import redis
import json
from abc import ABC, abstractmethod
from typing import Optional
from app.config import Config
from app.models import Timer

class Database(ABC):
    '''
    Abstract class for database.
    '''
    @abstractmethod
    def save_timer(self, timer: Timer) -> None:
        pass

    @abstractmethod
    def get_timer(self, timer_id: str) -> Optional[Timer]:
        pass


class RedisDatabase(Database):
    """
    Abstraction layer to interact with Redis.
    """
    def __init__(self):
        self.client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)
        
    def save_timer(self, timer: Timer) -> None:
        timer_id = str(timer.id)
        timer_data = timer.model_dump_json()
        
        self.client.set(f"timer:{timer_id}", timer_data)

    def get_timer(self, timer_id: str) -> Optional[Timer]:
        timer_data = self.client.get(f"timer:{timer_id}")
        if timer_data is None:
            return None
        return Timer(**json.loads(timer_data))
