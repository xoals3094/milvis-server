from datetime import datetime
from typing import List
from domain.schedule.domain.bus.BusSchedule import BusSchedule
from domain.schedule.dao.bus.BusScheduleDao import BusScheduleDao
from domain.schedule.dao.train.TrainScheduleCacher import TrainScheduleCacher
from domain.schedule.dao.train.TrainScheduleDao import TrainScheduleDao
from domain.schedule.domain.train.TrainSchedule import TrainSchedule
from app import exceptions


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
        cache_id = depart_station_code + arrive_station_code + depart_datetime.strftime('%Y%m%d')
        train_schedules = self.train_schedule_cacher.get(cache_id)
        if train_schedules is not None:
            return self._slice_schedules(depart_datetime, train_schedules)

        train_schedules = await self.train_schedule_dao.find_train_schedules(depart_station_code, arrive_station_code, depart_datetime)
        if len(train_schedules) == 0:
            raise exceptions.DataNotFound

        train_schedules.sort(key=lambda train_schedule: train_schedule.depart_time)
        self.train_schedule_cacher.set(cache_id, train_schedules)
        return self._slice_schedules(depart_datetime, train_schedules)

    def _slice_schedules(self, depart_datetime: datetime, train_schedules: List[TrainSchedule]):
        depart_time = depart_datetime.time()
        for i, train_schedule in enumerate(train_schedules):
            if train_schedule.depart_time > depart_time:
                return train_schedules[i:]

        return train_schedules
