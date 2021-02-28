# celery.py
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab # scheduler
from django.conf import settings

# default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','spaceindustry.settings')
app = Celery('spaceindustry')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

