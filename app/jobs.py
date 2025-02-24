import httpx
from datetime import datetime, timedelta
from rq import Queue
from app.dependencies import get_db
from app.models import Timer
from app.database import Database


def _set_timer_to_executed(timer:Timer):
    db = get_db()
    timer.is_executed = True
    db.save_timer(timer)

# trigger_webhook cant be a method of TimerService class because redis_queue.enqueue() throws
# TypeError: cannot pickle '_thread.lock' object otherwise
def trigger_webhook(timer: Timer):
    response = httpx.post(
        url=str(timer.webhook_url), 
        data={"id": timer.id})

    _set_timer_to_executed(timer)

    return response.status_code    

class TimerSerivce:
    def __init__(self, db: Database, redis_queue: Queue):
        self.db = db
        self.redis_queue = redis_queue

    def schedule_timer(self, timer: Timer):
        self.redis_queue.enqueue_at(timer.timestamp, trigger_webhook, timer)

    def process_expired_timers(self):
        timers = self.db.get_all_timers()
        print(f"Processing {len(timers)} timers")
        for timer in timers:
            if timer.timestamp <= datetime.now() and not timer.is_executed:
                print(f"Enqueueing webhook trigger for timer {timer.id}")
                self.redis_queue.enqueue(trigger_webhook, timer)
