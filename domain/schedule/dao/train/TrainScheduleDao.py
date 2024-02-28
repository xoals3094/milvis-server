import xml.etree.ElementTree as ET
import requests
from typing import List
from functools import partial
import asyncio
from abc import *
from datetime import datetime
from domain.schedule.domain.train.TrainSchedule import TrainSchedule
from config.api import SERVICE_KEY

trains = [{'id': '00', 'name': 'KTX'}, {'id': '01', 'name': '새마을호'}, {'id': '02', 'name': '무궁화호'},
          {'id': '03', 'name': '통근열차'}, {'id': '04', 'name': '누리로'}, {'id': '06', 'name': 'AREX직통'},
          {'id': '07', 'name': 'KTX-산천(A-type)'}, {'id': '08', 'name': 'ITX-새마을'}, {'id': '09', 'name': 'ITX-청춘'},
          {'id': '10', 'name': 'KTX-산천(B-type)'}, {'id': '16', 'name': 'KTX-이음'}, {'id': '17', 'name': 'SRT'}]
URL = 'http://apis.data.go.kr/1613000/TrainInfoService/getStrtpntAlocFndTrainInfo?serviceKey={SERVICE_KEY}&pageNo=1&numOfRows=100&_type=xml&depPlaceId={depart_station_code}&arrPlaceId={arrive_station_code}&depPlandTime={depart_datetime}&trainGradeCode={train_code}'


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
