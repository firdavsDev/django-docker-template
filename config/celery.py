import os

import cronitor.celery

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery monitoring (https://cronitor.io/)
_cronitor_api_key = os.environ.get("CRONITOR_API_KEY", "")
if _cronitor_api_key:
    cronitor.api_key = _cronitor_api_key
    cronitor.celery.initialize(app)
