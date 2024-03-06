from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from src.schedule_container import ScheduleContainer
from app import error_handling
from config import log
import logging
from logging.handlers import TimedRotatingFileHandler
datetime_format = "%Y-%m-%dT%H:%M:%S"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://milvis-front.vercel.app"
]

milvis_logger = logging.getLogger('milvis')
milvis_logger.setLevel(logging.INFO)

handler_filename = f'{log.INFO_LOG_PATH}/info_log.log'
handler = TimedRotatingFileHandler(filename=handler_filename, when='d', interval=1, backupCount=90, encoding='utf-8')
handler.suffix = log.SUFFIX
formatter = logging.Formatter(f'[%(levelname)s] %(asctime)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
milvis_logger.addHandler(handler)

warning_handler_filename = f'{log.WARNING_LOG_PATH}/warning_log.log'
waring_handler = TimedRotatingFileHandler(warning_handler_filename, when='d', interval=1, backupCount=90, encoding='utf-8')
waring_handler.suffix = log.SUFFIX
waring_formatter = logging.Formatter(f'[%(levelname)s] %(asctime)s %(message)s')
waring_handler.setFormatter(waring_formatter)
waring_handler.setLevel(logging.WARNING)
milvis_logger.addHandler(waring_handler)


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
