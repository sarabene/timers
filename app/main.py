from fastapi import FastAPI

from app.router import router
from app.jobs import process_expired_timers


def create_app():
    app = FastAPI(on_startup=[process_expired_timers])  #this runs only before the first request to the server but why?
    
    app.include_router(router)
    return app

app = create_app()
