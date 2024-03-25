class Train:
    def __init__(self, number, name):
        self.number = number
        self.name = name

    @property
    def json(self):
        return {
            'number': self.number,
            'name': self.name
        }

    @staticmethod
    def mapping(json):
        train = Train(number=json['number'], name=json['name'])
        return train


class TrainSchedule:
    def __init__(self, train: Train, depart_time, arrive_time):
        self.train = train
        self.depart_time = depart_time
        self.arrive_time = arrive_time

    @property
    def json(self):
        return {
            'train': self.train.json,
            'depart_time': self.depart_time,
            'arrive_time': self.arrive_time,
        }

    @staticmethod
    def mapping(json):
        train_json = json['train']
        return TrainSchedule(
            train=Train.mapping(train_json),
            depart_time=json['depart_time'],
            arrive_time=json['arrive_time']
        )
