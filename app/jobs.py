import httpx
from datetime import datetime, timedelta
from rq import Queue
from app.dependencies import get_db
from app.models import Timer

redis_queue = Queue(connection=get_db().client)


def set_timer_to_executed(timer):
    db = get_db()
    timer.is_executed = True
    db.save_timer(timer)


def trigger_webhook(timer: Timer):
    # make a POST request to the webhook_url
    
    #response = httpx.post(
    #    url=timer.webhook_url, 
    #    data={"id": timer.id})


    print(
        f"Triggered webhook for timer {timer.id} at {timer.webhook_url}"
    )

    set_timer_to_executed(timer)

    #return response.status_code

def schedule_timer(timer: Timer):
    job = redis_queue.enqueue_at(timer.timestamp, trigger_webhook, timer)
    # handle error but how??


def process_expired_timers():
    db = get_db()
    timers = db.get_all_timers()
    print(f"Processing {len(timers)} timers")
    for timer in timers:
        if timer.timestamp <= datetime.now() and not timer.is_executed:
            print(f"Enqueueing webhook trigger for timer {timer.id}")
            redis_queue.enqueue(trigger_webhook, timer)
