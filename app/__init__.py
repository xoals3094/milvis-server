from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from src.schedule_container import ScheduleContainer
from app import error_handling
from .handler_setting import set_handler
from etc.webhook import discord_webhook
import logging
datetime_format = "%Y-%m-%dT%H:%M:%S"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://milvis-front.vercel.app"
]

milvis_logger = logging.getLogger('milvis')
milvis_logger.setLevel(logging.INFO)

set_handler(milvis_logger, logging.INFO)
set_handler(milvis_logger, logging.WARNING)


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

    @app.middleware('http')
    async def write_log(request: Request, call_next):
        body = await request.body()
        try:
            response = await call_next(request)
        except Exception as e:
            msg = f'[{request.method}] {request.url}\n{body.decode()}'
            milvis_logger.exception(msg, exc_info=e)
            discord_webhook.send_webhook(request.url.path, request.method, e)
            raise e

        msg = f'[{request.method}] {request.url} {response.status_code}'
        milvis_logger.info(msg)

        return response

    return app
