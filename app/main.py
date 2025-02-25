from fastapi import FastAPI
from app.router import router


def create_app():
    app = FastAPI()
    app.include_router(router)
    return app

app = create_app()
