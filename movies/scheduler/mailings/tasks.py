import logging

from config.celery import app

logger = logging.getLogger(__name__)


@app.task(name="task_send_mailings")
def task_send_mailings(*args, **kwargs) -> None:
    logger.warning(",".join(str(arg) for arg in args) + "; " + ",".join(f"{k}={v}" for k, v in kwargs.items()))
