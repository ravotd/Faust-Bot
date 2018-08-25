import sys
from logging import StreamHandler, Formatter, getLogger, Logger, DEBUG, INFO


def get_stream_handler() -> StreamHandler:
    handler = StreamHandler(sys.stdout)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


_logger = getLogger(__name__)
_logger.addHandler(get_stream_handler())
_logger.setLevel(DEBUG)
debug = True
logger_map = {}


def enable_debug_mode(enabled: bool = True):
    global debug
    if enabled:
        debug = True
        _logger.debug('Debugging log enabled!')
    else:
        debug = False
        _logger.debug('Debugging log disabled!')


def get_logger(name: str) -> Logger:
    global debug
    if name not in logger_map:
        logger = getLogger(name)
        logger.addHandler(get_stream_handler())
        if debug:
            logger.setLevel(DEBUG)
        else:
            logger.setLevel(INFO)
        logger_map[name] = logger
    return logger_map[name]
