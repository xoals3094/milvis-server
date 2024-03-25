from datetime import time


class Line:
    def __init__(self, name):
        self.name = name

    @property
    def json(self):
        return {
            'name': self.name
        }


class BusSchedule:
    def __init__(self, line: Line, depart_time: time, arrive_time: time, direction: str, section: str):
        self.line = line
        self.depart_time = depart_time
        self.arrive_time = arrive_time
        self.direction = direction
        self.section = section

    @property
    def json(self):
        return {
            'line': self.line.json,
            'depart_time': self.depart_time,
            'arrive_time': self.arrive_time,
            'direction': self.direction,
            'section': self.section
        }

    @staticmethod
    def mapping(json):
        return BusSchedule(
            line=Line(json['line']['name']),
            depart_time=json['depart_time'],
            arrive_time=json['arrive_time'],
            direction=json['direction'],
            section=json['section'])
