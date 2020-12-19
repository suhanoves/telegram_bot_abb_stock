import logging
import sys
from typing import List

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: str = "DEBUG", ignored: List[str] = ""):
    logging.basicConfig(level=level, handlers=[InterceptHandler()])
    for ignore in ignored:
        logger.disable(ignore)
    logger.info('Logging is successfully configured')


logger.remove()

logger.add(sys.stderr, level='DEBUG',
           format='<green>{time:DD.MM.YYYY HH:mm:ss.SSS}</green>'
                  ' | <level>{level: <8}</level>'
                  ' | <level>{message}</level>',
           filter=None, colorize=None, serialize=False, backtrace=True, diagnose=True, enqueue=False, catch=True)

# TODO change path to log. Take it from environment
logger.add('../../logs/warning.log', level='WARNING',
           format='{time:DD.MM.YYYY HH:mm:ss.SSS} | {message} | {level: <8} | {name}:{function}:{line}',
           filter=None, colorize=None, serialize=False, backtrace=True, diagnose=True, enqueue=False, catch=True)
