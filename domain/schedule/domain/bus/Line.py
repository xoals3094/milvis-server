class Line:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }