import random
import time

from faker import Faker
from flask import Flask, render_template, jsonify, url_for, request
from celery import Celery


flask_app = Flask(__name__)
celery_app = Celery(
    flask_app.name,
    broker="redis://52.81.228.173:16379/0",
    backend="redis://52.81.228.173:16379/1",
)


@flask_app.route('/')
def home():
    return render_template('progress.html')


@flask_app.route('/long_task', methods=['POST'])
def long_task():
    file_count = request.form.get('file_count', 100, type=int)
    task = copy_s3_files.apply_async(args=[file_count])
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id)}


@flask_app.route('/status/<task_id>')
def task_status(task_id):
    task = copy_s3_files.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@celery_app.task(bind=True)
def copy_s3_files(self, files_count):
    # 模拟copy s3文件
    fake = Faker()
    for i in range(files_count):
        # time.sleep(random.randint(1, 5))
        time.sleep(random.random())
        meta = {
            'current': i + 1,
            'total': files_count,
            'status': '{}-{}.xlsx'.format(fake.name(), i + 1)
        }
        self.update_state(state='PROGRESS', meta=meta)
    return {'current': files_count, 'total': files_count, 'status': 'Task completed!', 'result': files_count}


if __name__ == '__main__':
    flask_app.run()
