### About

在复制许多s3文件时，可能要花很多时间，因此使用celery异步实现。  

同时借鉴http://www.pythondoc.com/flask-celery/first.html,
在html页面实现异步任务进度条。

---

### Run
 - `celery worker -A app.celery_app --loglevel=debug -P threads`
 - `python app.py`
