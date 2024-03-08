from exceptions.DefaultException import DefaultException


class PersistenceException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ResourceNotFoundException(PersistenceException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ConnectionException(PersistenceException):
    def __init__(self, msg):
        super().__init__(msg=msg)
