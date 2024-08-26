from celery import Celery
from configs.db import REDIS_HOST, REDIS_PORT

celery_app = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
)

# Optional configuration, for example timezone
celery_app.conf.update(timezone="UTC")

celery_app.autodiscover_tasks(["tasks.files"], force=True)
