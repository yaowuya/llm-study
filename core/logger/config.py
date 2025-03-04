import os.path
import sys

from core.settings import settings

CONSOLE_HANDLER = "console"
ROOT_HANDLER = "root"
ERROR_HANDLER = "error"
CELERY_HANDLER = "celery"

HANDLERS = {
    CONSOLE_HANDLER: {
        "sink": sys.stdout,
        "level": settings.logging_level,
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {thread.name} | "
        "<level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>"
        ":<cyan>{line}</cyan> - <level>{message}</level>",
    },
    ROOT_HANDLER: {
        "sink": os.path.join(settings.logging_dir, "server.log"),
        "level": settings.logging_level,
        "enqueue": True,  # 多进程安全
        "rotation": "100 MB",  # 日志文件最大大小
        "retention": "1 week",  # 日志保留时间
        "encoding": "utf-8",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} "
        ": {function}:{line} -  {message}",
    },
    ERROR_HANDLER: {
        "sink": os.path.join(settings.logging_dir, "error.log"),
        "enqueue": True,
        "level": "ERROR",
        "retention": "1 week",
        "rotation": "100 MB",
        "encoding": "utf-8",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} "
        ": {function}:{line} -  {message}",
    },
    CELERY_HANDLER: {
        "sink": os.path.join(settings.logging_dir, "celery.log"),
        "level": settings.logging_level,
        "enqueue": True,  # 多进程安全
        "rotation": "200 MB",  # 日志文件最大大小
        "retention": "1 week",  # 日志保留时间
        "encoding": "utf-8",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | {module} "
        ": {function}:{line} -  {message}",
        "filter": lambda x: x["extra"].get("name") == "celery",
    },
}

LOGURU_CONFIG = {
    "handlers": [HANDLERS[CONSOLE_HANDLER], HANDLERS[ROOT_HANDLER], HANDLERS[ERROR_HANDLER], HANDLERS[CELERY_HANDLER]],
}

LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")
