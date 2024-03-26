

# Это позволит убедиться, что экземпляр приложения Celery всегда импортируется
# когда Django запускается, чтобы shared_task использовал этот экземпляр.
from .celery import app as celery_app

all = ('celery_app',)
