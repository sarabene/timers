import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_db, get_redis_queue
from app.database import Database
from app.models import Timer, TimerRequest
from app.jobs import TimerSerivce
from app.queue import JobQueue

router = APIRouter()

@router.post("/timer")
def create_timer(request: TimerRequest, db: Database = Depends(get_db), redis_queue: JobQueue = Depends(get_redis_queue)):
    '''
    Endpoint to create and schedule a timer.
    Parameters:
        - "hours" (int): no. of hours to wait before triggering the webhook
        - "minutes" (int): no. of minutes to wait before triggering the webhook
        - "seconds" (int): no. of seconds to wait before triggering the webhook
        - "webhook_url" (url): the url the webhook should be sent to
    '''
    try:
        time_delta= datetime.timedelta(
            hours=request.hours,
            minutes=request.minutes,
            seconds=request.seconds
        )
        timer = Timer(
            webhook_url=request.webhook_url,
            timestamp=datetime.datetime.now() + time_delta)
    
    except OverflowError:
        raise HTTPException(status_code=422, detail="Invalid time duration, try a shorter duration")
    
    # add timer to task queue
    timer_service = TimerSerivce(redis_queue)
    timer_service.schedule_timer(timer)

    db.save_timer(timer)

    return {
        "message": "Timer created",
        "id": timer.id,
        "time_left": time_delta.total_seconds(),
    }


@router.get("/timer/{timer_id}")
def get_timer(timer_id: str, db: Database = Depends(get_db)):
    '''
    Endpoint to get the remaining time left for a timer.
    Parameters:
        timer_id (str): the id of the timer
    '''

    timer = db.get_timer(timer_id)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")

    time_left = (timer.timestamp - datetime.datetime.now()).total_seconds()
    return {
        "id": timer.id,
        "time_left": max(0, time_left)
    }
