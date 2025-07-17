# social_bot/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_bot.settings')

app = Celery('social_bot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
