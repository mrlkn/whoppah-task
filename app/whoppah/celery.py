import os

from celery import Celery
from django.conf import settings

app = Celery("whoppah")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whoppah.settings")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
