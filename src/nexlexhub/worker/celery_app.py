from __future__ import annotations

from celery import Celery

from nexlexhub.core.config import get_settings


settings = get_settings()
celery_app = Celery("nexlexhub", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_default_queue = "nexlexhub"


@celery_app.task
def ping() -> str:
    return "pong"
