import httpx
from abc import ABC, abstractmethod
from rq import Queue
from app.models import Timer


def trigger_webhook(timer: Timer):
    try:
        response = httpx.post(
            url=str(timer.webhook_url), 
            data={"id": timer.id})

        return response.status_code

    except httpx.HTTPError as e:
        pass

class JobQueue(ABC):
    '''
    Abstract class for job queue.
    '''
    @abstractmethod
    def schedule_job_for_timer(self):
        pass

class RedisQueue(JobQueue):
    """
    Abstraction layer to interact with Redis-Queue.
    """
    def __init__(self, redis_connection, **kwargs):
        self.queue = Queue(connection=redis_connection, **kwargs)

    def schedule_job_for_timer(self, timer):
        job = self.queue.enqueue_at(timer.timestamp, trigger_webhook, timer)
        return job
