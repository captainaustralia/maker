import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maker.settings')

app = Celery('maker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-inactive-users-every-day': {
        'task': 'core.tasks.delete_inactive_beat',
        'schedule': crontab(minute=30, hour=0),
    },
}

# celery -A maker worker -l info
# celery -A maker beat -l info
