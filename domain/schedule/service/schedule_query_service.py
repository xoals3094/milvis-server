from domain.schedule.dto.bus_schedule import BusSchedule
from domain.schedule.dto.train_schedule import TrainSchedule
from domain.schedule.dao.bus_schedule_dao import BusScheduleDao
from domain.schedule.dao.train_schedule_cacher import TrainScheduleCacher
from domain.schedule.dao.train_schedule_dao import TrainScheduleDao
from domain.schedule.util import schedule_util

from datetime import datetime
from typing import List


class ScheduleQueryService:
    def __init__(self,
                 bus_schedule_dao: BusScheduleDao,
                 train_schedule_cacher: TrainScheduleCacher,
                 train_schedule_dao: TrainScheduleDao):
        self.bus_schedule_dao = bus_schedule_dao
        self.train_schedule_cacher = train_schedule_cacher
        self.train_schedule_dao = train_schedule_dao

    def get_bus_schedules(self, direction, section, depart_datetime: datetime) -> List[BusSchedule]:
        depart_time = depart_datetime.time()
        return self.bus_schedule_dao.find_bus_schedule(direction, section, depart_time)

    async def get_train_schedules(self, depart_station_code, arrive_station_code, depart_datetime: datetime) -> List[TrainSchedule]:
        train_schedules = self.train_schedule_cacher.get(depart_station_code, arrive_station_code, depart_datetime)
        if train_schedules is not None:
            train_schedules = schedule_util.slicer(depart_datetime, train_schedules)
            return train_schedules

        train_schedules = await self.train_schedule_dao.find_train_schedules(depart_station_code, arrive_station_code, depart_datetime)
        self.train_schedule_cacher.set(depart_station_code, arrive_station_code, depart_datetime, train_schedules)

        train_schedules = schedule_util.slicer(depart_datetime, train_schedules)
        return train_schedules
