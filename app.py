import random
import time

from celery import Celery

celery_app = Celery(
    "app",
    broker="redis://52.81.228.173:16379/0",
    backend="redis://52.81.228.173:16379/1",
)


@celery_app.task
def add(x, y):
    time.sleep(random.randint(3, 6))
    return x + y


if __name__ == '__main__':
    celery_app.start()
