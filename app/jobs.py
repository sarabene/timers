import httpx
from rq import Queue
from app.models import Timer

# trigger_webhook cant be a method of TimerService class because redis_queue.enqueue() throws
# TypeError: cannot pickle '_thread.lock' object otherwise
def trigger_webhook(timer: Timer):
    try:
        response = httpx.post(
            url=str(timer.webhook_url), 
            data={"id": timer.id})

        return response.status_code

    except httpx.HTTPError as e:
        pass
    
class TimerSerivce:
    def __init__(self, redis_queue: Queue):
        self.redis_queue = redis_queue

    def schedule_timer(self, timer: Timer):
        job = self.redis_queue.enqueue_at(timer.timestamp, trigger_webhook, timer)
