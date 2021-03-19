### About

一个简单的Celery任务队列Demo，模拟以异步的方式复制大量S3文件，拿来简单改改就能换成别的任务。

同时借鉴[FlaskCelery](http://www.pythondoc.com/flask-celery/first.html)里的例子，在html页面展示任务进度条。

---

### Run
 - `celery worker -A app.celery_app --loglevel=debug -P threads`
 - `python app.py`
