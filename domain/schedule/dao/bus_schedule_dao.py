from domain.schedule.dto.bus_schedule import BusSchedule
from typing import List
from datetime import datetime, time
from abc import *


class BusScheduleDao(metaclass=ABCMeta):
    @abstractmethod
    def find_bus_schedule(self, direction, section, depart_time: time) -> List[BusSchedule]:
        pass


class MongoDBBusScheduleDao(BusScheduleDao):
    def __init__(self, connection):
        self.db = connection['milvis']

    def find_bus_schedule(self, direction, section, depart_time: time) -> List[BusSchedule]:
        find = {
            'direction': direction,
            'section': section,
            'depart_time': {
                '$gte': datetime(year=1, month=1, day=1, hour=depart_time.hour, minute=depart_time.minute, second=depart_time.second)
            }
        }
        bus_schedules_json = list(self.db.schedule.find(find))
        for bus_schedule_json in bus_schedules_json:
            bus_schedule_json['depart_time'] = bus_schedule_json['depart_time'].time()
            bus_schedule_json['arrive_time'] = bus_schedule_json['arrive_time'].time()
        bus_schedules = [BusSchedule.mapping(bus_schedule_json) for bus_schedule_json in bus_schedules_json]
        return bus_schedules
