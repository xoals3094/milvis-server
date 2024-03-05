from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from src.schedule_container import ScheduleContainer
from app import error_handling
datetime_format = "%Y-%m-%dT%H:%M:%S"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://milvis-front.vercel.app"
]


def create_app():
    ScheduleContainer()

    app = FastAPI()
    error_handling.error_handling(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    return app
