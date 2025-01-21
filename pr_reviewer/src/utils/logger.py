import logging
from pythonjsonlogger.json import JsonFormatter
from logging import Logger


def get_logger() -> Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger
