import logging
from config import log
from logging.handlers import TimedRotatingFileHandler


def set_handler(logger, level):
    filename = log.INFO_LOG_FILENAME
    if level == logging.WARNING:
        filename = log.WARNING_LOG_FILENAME

    handler = TimedRotatingFileHandler(filename=filename, when='d', interval=1, backupCount=90, encoding='utf-8')
    handler.suffix = log.SUFFIX
    formatter = logging.Formatter(log.LOG_FORMAT)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
