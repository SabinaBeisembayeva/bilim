import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilim.settings')

app = Celery('bilim', backend='rpc://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    # 'add-every-monday-morning': {
    #     'task': 'Place.tasks.offline_tasks',
    #     'schedule': crontab(minute='*')
    # },
    # 'check-every-day-active-packet': {
    #     'task': 'Place.tasks.check_activation_packet',
    #     'schedule': crontab(hour=10, minute=59)
    # }
}