import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    env: str = "prod"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open_api_key: str = ""

    logging_dir: str = os.path.join(base_dir, "logs")
    logging_level: str = "INFO"

    celery_broker: str = "redis://:@localhost:6379/0"
    celery_backend: str = "redis://:@localhost:6379/13"
    celery_result_expires: int = 60 * 60 * 24 * 7  # 默认7天
    redis_url: str = "redis://:123456@localhost?db=1"
    max_thread_num: int = 16
    secret_key: bytes = b"78f40f2cffeee727a4be179049cecf89"

    class Config:
        env_file = ".env"


settings = Settings()
