import logging

from core.logger import logger
from core.logger.config import LOGGER_NAMES, LOGURU_CONFIG
from core.logger.handlers import InterceptHandler


class InitService(object):
    _init = False

    def __call__(self, *args, **kwargs):
        if not self.__class__._init:
            # 把自定义模块写入到环境变量中,方便模块寻找
            _init_logger()
            self.__class__._init = True


def _init_logger():
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
    logger.configure(**LOGURU_CONFIG)


init_service = InitService()
