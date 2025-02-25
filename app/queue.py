from abc import ABC, abstractmethod
from rq import Queue

class JobQueue(ABC):
    @abstractmethod
    def schedule_job_at(self):
        pass

class RedisQueue(JobQueue):
    def __init__(self, redis_connection, **kwargs):
        self.queue = Queue(connection=redis_connection, **kwargs)

    def schedule_job_at(self, timestamp, callback_func, *args):
        job = self.queue.enqueue_at(timestamp, callback_func, *args)
        return job
