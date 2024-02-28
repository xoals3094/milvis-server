class BaseException(Exception):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    @property
    def json(self):
        return {
            'msg': self.msg,
            'code': self.code
        }

class DataNotFound(BaseException):
    def __init__(self, msg='일치하는 데이터를 찾을 수 없습니다', code=100):
        self.msg = msg
        self.code = code
