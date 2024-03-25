from domain.schedule.dto.train_schedule import TrainSchedule

import redis
import json

from typing import List
from datetime import datetime

from abc import *


class TrainScheduleCacher(metaclass=ABCMeta):
    @abstractmethod
    def get(self, depart_station_code, arrive_station_code, depart_datetime: datetime):
        pass

    @abstractmethod
    def set(self, depart_station_code, arrive_station_code, depart_datetime: datetime, train_schedules):
        pass


class RedisTrainScheduleCacher(TrainScheduleCacher):
    def __init__(self, redis_connection: redis.StrictRedis):
        self.db = redis_connection

    def _create_cache_id(self, depart_station_code, arrive_station_code, depart_datetime: datetime):
        return depart_station_code + arrive_station_code + depart_datetime.strftime('%Y%m%d')

    def get(self, depart_station_code, arrive_station_code, depart_datetime: datetime):
        cache_id = self._create_cache_id(depart_station_code, arrive_station_code, depart_datetime)

        train_schedules = self.db.get(cache_id)
        if train_schedules is None:
            return None
        schedules_json = json.loads(str(train_schedules))
        for schedule_json in schedules_json:
            schedule_json['depart_time'] = datetime.strptime(schedule_json['depart_time'], '%H%M%S').time()
            schedule_json['arrive_time'] = datetime.strptime(schedule_json['arrive_time'], '%H%M%S').time()

        return [TrainSchedule.mapping(schedule_json) for schedule_json in schedules_json]

    def set(self, depart_station_code, arrive_station_code, depart_datetime: datetime, train_schedules: List[TrainSchedule]):
        cache_id = self._create_cache_id(depart_station_code, arrive_station_code, depart_datetime)

        train_schedules_json = []
        for train_schedule in train_schedules:
            train_schedule_json = train_schedule.json
            train_schedule_json['depart_time'] = train_schedule_json['depart_time'].strftime('%H%M%S')
            train_schedule_json['arrive_time'] = train_schedule_json['arrive_time'].strftime('%H%M%S')
            train_schedules_json.append(train_schedule_json)

        self.db.set(cache_id, json.dumps(train_schedules_json), ex=3600)
