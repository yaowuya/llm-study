import uvicorn

from apps.study.url import study_api
from core.bootstrap import BootStrap
from core.settings import settings

bootstrap = BootStrap(
    app_name="FastAPI-Study",
    app_version="0.1.0",
    routers=[study_api],
)
bootstrap.boot()

if __name__ == "__main__":
    if settings.env == "dev":
        uvicorn.run(
            app="main:bootstrap.application",
            host=settings.app_host,
            port=settings.app_port,
            reload=True,
            log_level="debug",  # 使用这个替代 debug=True
        )
    else:
        uvicorn.run(
            app="main:bootstrap.application",
            host=settings.app_host,
            port=settings.app_port,
            reload=False,
            debug=False,
            log_level="info",
        )
