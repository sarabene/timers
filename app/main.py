from fastapi import FastAPI

from app.router import router
from app.jobs import TimerSerivce
from app.dependencies import get_db, get_redis_queue

def initialize_timer_service():
    timer_service = TimerSerivce(get_db(), get_redis_queue())
    timer_service.process_expired_timers()
    

def create_app():
    app = FastAPI()
    app.include_router(router)
    initialize_timer_service()

    return app

app = create_app()
