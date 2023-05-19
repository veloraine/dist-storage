import os
from kombu import Queue

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dist_storage.settings')
app = Celery('tasks', backend='redis://redis:6379',
             broker='redis://redis:6379')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default',    routing_key='task.#'),
    Queue('timer_election', routing_key='election.#'),
    Queue('timer_heartbeat', routing_key='heartbeat.#'),
)
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'task.default'

app.conf.task_routes = {
    'storage.timer.heartbeat': {
        'queue': 'timer_heartbeat',
        'routing_key': 'heartbeat.timer',
    },
    'storage.timer.election': {
        'queue': 'timer_election',
        'routing_key': 'election.timer',
    },
}
