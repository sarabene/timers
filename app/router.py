from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta

from app.models import Timer, TimerRequest
from app.database import Database
from app.dependencies import get_db
from app.jobs import schedule_timer

router = APIRouter()

@router.post("/timer")
def create_timer(request: TimerRequest, db: Database = Depends(get_db)):
    time_delta= timedelta(
        hours=request.hours,
        minutes=request.minutes,
        seconds=request.seconds
    )

    # TO DO assume utc timezone
    timer = Timer(
        webhook_url=request.webhook_url,
        timestamp=datetime.now() + time_delta)
    
    # commit timer to database
    db.save_timer(timer)

    # add timer to task queue
    schedule_timer(timer)
    #return 500 id error?

    return {
        "message": "Timer created",
        "id": timer.id,
        "time_left": time_delta.total_seconds(),
    }


@router.get("/timer/{timer_uuid}")
def get_timer(timer_uuid, db: Database = Depends(get_db)):
    # handle different uuid formats

    # get timer from database
    timer = db.get_timer(timer_uuid)
    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")

    time_left = (timer.timestamp - datetime.now()).total_seconds()
    return {
        "id": timer.id,
        "time_left": max(0, time_left)
    }
