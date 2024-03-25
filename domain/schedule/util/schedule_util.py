from domain.schedule.dto.TrainSchedule import TrainSchedule
from datetime import datetime
from typing import List


def slicer(depart_datetime: datetime, train_schedules: List[TrainSchedule]):
    depart_time = depart_datetime.time()
    for i, train_schedule in enumerate(train_schedules):
        if train_schedule.depart_time > depart_time:
            return train_schedules[i:]

    return train_schedules
