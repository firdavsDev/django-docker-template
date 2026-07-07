import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Celery monitoring (https://cronitor.io/) — enabled only when an API key is set
CRONITOR_API_KEY = os.environ.get("CRONITOR_API_KEY")
if CRONITOR_API_KEY:
    import cronitor.celery

    cronitor.api_key = CRONITOR_API_KEY
    cronitor.celery.initialize(app)
