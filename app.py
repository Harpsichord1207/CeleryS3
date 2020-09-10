from __future__ import absolute_import
import random
import time

from celery import Celery

app = Celery(
    "Test",
    broker="redis://52.81.228.173:16379/",
    backend="redis://52.81.228.173:16379/",
    include=['app']
)


@app.task
def add(x, y):
    time.sleep(random.randint(3, 6))
    return x + y


if __name__ == '__main__':
    app.start()
