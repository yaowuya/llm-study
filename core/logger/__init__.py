from loguru import logger as loguru_logger

logger = loguru_logger
celery_logger = loguru_logger.bind(name="celery")
