import logging

DEBUG = 10
PRODUCTION = 20
_logger = logging.getLogger(__name__)
level = 0
logger_map = {}


def enable_debug_mode(enabled: bool = True):
    if enabled:
        level = DEBUG
    else:
        level = PRODUCTION


def get_logger(name: str) -> logging.Logger:
    if name not in logger_map:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger_map[name] = logger
    return logger_map[name]
