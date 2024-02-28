from domain.schedule.domain.train.TrainSchedule import TrainSchedule

import redis
import json

from typing import List
from datetime import datetime

from abc import *


class TrainScheduleCacher(metaclass=ABCMeta):
    @abstractmethod
    def get(self, cache_id):
        pass

    @abstractmethod
    def set(self, cache_id, train_schedules):
        pass


class RedisTrainScheduleCacher(TrainScheduleCacher):
    def __init__(self, redis_connection: redis.StrictRedis):
        self.db = redis_connection

    def get(self, cache_id):
        train_schedules = self.db.get(cache_id)
        if train_schedules is None:
            return None
        schedules_json = json.loads(str(train_schedules))
        for schedule_json in schedules_json:
            schedule_json['depart_time'] = datetime.strptime(schedule_json['depart_time'], '%H%M%S').time()
            schedule_json['arrive_time'] = datetime.strptime(schedule_json['arrive_time'], '%H%M%S').time()

        return [TrainSchedule.mapping(schedule_json) for schedule_json in schedules_json]

    def set(self, cache_id, train_schedules: List[TrainSchedule]):
        train_schedules_json = []
        for train_schedule in train_schedules:
            train_schedule_json = train_schedule.json
            train_schedule_json['depart_time'] = train_schedule_json['depart_time'].strftime('%H%M%S')
            train_schedule_json['arrive_time'] = train_schedule_json['arrive_time'].strftime('%H%M%S')
            train_schedules_json.append(train_schedule_json)

        self.db.set(cache_id, json.dumps(train_schedules_json), ex=3600)
