from fastapi import APIRouter
from .schedule import schedule_router

api_router = APIRouter(prefix='/api')
api_router.include_router(schedule_router)
