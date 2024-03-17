

# NOT FUNCTIONAL - NEEDS TO BE REFACTORED

from celery import Celery
from celery.schedules import crontab
# from django.conf import settings
from ProjectX import settings

app = Celery('expiration_monitor')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'monitor_ssl_certificates': {
        'task': 'sslmonitor.tasks.monitor_ssl_certificates',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
