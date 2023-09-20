import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'app.settings')
app = Celery("app")
# app.conf.task_routes = {
#     'user.tasks.task2': {'queue': 'mailQueue'},
#     'user.tasks.task3': {'queue': 'queue2'}
# }
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),
    'sep': ':',
    'queue_order_strategy': 'priority',
}

app.autodiscover_tasks()
