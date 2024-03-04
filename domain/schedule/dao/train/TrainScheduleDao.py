from domain.schedule.domain.train.TrainSchedule import TrainSchedule

from typing import List
from datetime import datetime
from functools import partial
from abc import *
from config.api import SERVICE_KEY, URL
from etc.train_info import trains

import xml.etree.ElementTree as ET
import requests
import asyncio

from exceptions import PersistenceException


class TrainScheduleDao(metaclass=ABCMeta):
    @abstractmethod
    async def find_train_schedules(self, depart_station_code, arrive_station_code, depart_datetime) -> List[TrainSchedule]:
        pass


class ExternalTrainScheduleDao(TrainScheduleDao):
    async def find_train_schedules(self, depart_station_code, arrive_station_code, depart_datetime: datetime) -> List[TrainSchedule]:
        results = await asyncio.create_task(self._find_train_schedules(depart_station_code, arrive_station_code, depart_datetime))
        train_schedules = []
        for result in results:
            train_schedules += result

        if len(train_schedules) == 0:
            raise PersistenceException.ResourceNotFoundException(msg='일치하는 기차 데이터를 찾을 수 없습니다')

        train_schedules.sort(key=lambda train_schedule: train_schedule.depart_time)

        return train_schedules

    async def _find_train_schedules(self, depart_station_code, arrive_station_code, depart_datetime):
        fts = [asyncio.ensure_future(
            self._request_train_schedule(train['id'], depart_station_code, arrive_station_code, depart_datetime))
            for train in trains]

        return await asyncio.gather(*fts)

    async def _request_train_schedule(self, train_code, depart_station_code, arrive_station_code, depart_datetime: datetime):
        request_url = URL.format(
            SERVICE_KEY=SERVICE_KEY,
            depart_station_code=depart_station_code,
            arrive_station_code=arrive_station_code,
            depart_datetime=depart_datetime.strftime('%Y%m%d'),
            train_code=train_code)

        loop = asyncio.get_event_loop()
        request = partial(requests.get, request_url, verify=False)
        res = await loop.run_in_executor(None, request)

        root = ET.fromstring(res.text)
        body = root.find("body")
        items = body.find("items").findall('item')

        train_schedules = []
        for item in items:
            json = {
                'train': {
                    'number': item.find('trainno').text,
                    'name': item.find('traingradename').text,
                },
                'depart_time': datetime.strptime(item.find('depplandtime').text, '%Y%m%d%H%M%S').time(),
                'arrive_time': datetime.strptime(item.find('arrplandtime').text, '%Y%m%d%H%M%S').time()
            }
            train_schedules.append(TrainSchedule.mapping(json))
        return train_schedules
