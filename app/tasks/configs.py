from celery import Celery
from celery.schedules import crontab

from configs.db import REDIS_PORT, REDIS_HOST

celery_app = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
)

# Optional configuration, for example timezone
celery_app.conf.update(timezone="UTC")
