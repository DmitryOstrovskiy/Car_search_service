import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_search_service.settings')

app = Celery('car_search_service')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


