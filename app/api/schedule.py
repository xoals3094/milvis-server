from fastapi import APIRouter
from fastapi import Query, Depends
from pydantic import BaseModel, Field

from datetime import time, datetime
from enum import Enum
from typing import List

from dependency_injector.wiring import inject, Provide
from domain.schedule.service.ScheduleQueryService import ScheduleQueryService
from src.schedule_container import ScheduleContainer

schedule_router = APIRouter(prefix='/schedule')


class Direction(str, Enum):
    station = 'STATION'
    campus = 'CAMPUS'


class Section(str, Enum):
    weekday = 'WEEKDAY'
    holiday = 'HOLIDAY'
    campus_only = 'CAMPUS-ONLY'


class Line(BaseModel):
    id: str = Field(title='출발 시간', examples=['MYB1'])
    name: str = Field(title='노선명', examples=['용성1'])


class BusSchedule(BaseModel):
    line: Line
    depart_time: time = Field(title='출발 시간', examples=[datetime.now().time()])
    arrive_time: time = Field(title='도착 시간', examples=[datetime.now().time()])
    direction: str = Field(title='방향', examples=[Direction.campus])
    section: str = Field(title='구분', examples=[Section.weekday])


class BusScheduleResponse(BaseModel):
    direction: str = Field(title='방향', examples=[Direction.campus])
    schedules: List[BusSchedule]


@schedule_router.get(path='/bus', summary='버스 일정 조회',
                     status_code=200,
                     response_model=BusScheduleResponse,
                     tags=['schedule'])
@inject
async def bus_schedule(direction: Direction = Query(description='조회할 방향'),
                       section: Section = Query(description='구분'),
                       depart_datetime: datetime = Query(description='조회할 시간(yyyy-mm-ddTHH:MM:SS)', example=datetime.now()),
                       schedule_query_service: ScheduleQueryService = Depends(Provide[ScheduleContainer.schedule_query_service])):
    bus_schedules = schedule_query_service.get_bus_schedules(direction, section, depart_datetime)
    return {
        'direction': direction,
        'schedules': [bus_schedule.json for bus_schedule in bus_schedules]
    }


class Train(BaseModel):
    number: str = Field(title='기차 이름', examples=['무궁화호'])
    name: str = Field(title='기차 번호', examples=['213'])


class TrainSchedule(BaseModel):
    train: Train
    depart_time: time = Field(title='출발 시간', examples=[datetime.now().time()])
    arrive_time: time = Field(title='도착 시간', examples=[datetime.now().time()])


class TrainScheduleResponse(BaseModel):
    schedules: List[TrainSchedule]


@schedule_router.get(path='/train', summary='기차 시간 조회',
                     status_code=200,
                     response_model=TrainScheduleResponse,
                     tags=['schedule'])
@inject
async def query_train_schedule(depart_station_code: str = Query(description='출발역 코드', example='NAT013841'),
                               arrive_station_code: str = Query(description='도착역 코드', example='NAT010000'),
                               depart_datetime: datetime = Query(description='출발 날짜(yyyy-mm-ddTHH:MM:SS)', example=datetime.now()),
                               schedule_query_service: ScheduleQueryService = Depends(Provide[ScheduleContainer.schedule_query_service])):
    train_schedules = await schedule_query_service.get_train_schedules(depart_station_code, arrive_station_code, depart_datetime)
    return {'schedules': [train_schedule.json for train_schedule in train_schedules]}
