import os
from celery import Celery

# Установите переменную среды Django для настроек 'myproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_search_service.settings')

app = Celery('car_search_service')

# Используйте строку 'django.conf:settings', чтобы Celery загрузил любые пользовательские настройки из проекта Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите модуль 'tasks.py' в django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')