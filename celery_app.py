from celery import Celery
from src.core.pydantic_config import config


broker = f"{config.REDIS_URL}/0"
backend = f"{config.REDIS_URL}/1"
celery_app = Celery('quriya', broker=broker, backend=backend)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    include=['src.tasks.email_task',
             ]
)


# celery_app.autodiscover_tasks(["src.tasks"])
