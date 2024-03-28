from car_search_service.celery import app
from .models import Truck, Location
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


@app.task
def update_truck_locations():
    logging.info('Начало задачи: обновление локаций грузовиков')
    try:
        locations = list(Location.objects.all())
        for truck in Truck.objects.all():
            new_location = random.choice(locations) if locations else None
            if new_location:
                truck.current_location = new_location
                truck.save()
        logging.info('Задача завершена успешно')
    except Exception as e:
        logging.error('Ошибка во время выполнения задачи: %s', e)


update_truck_locations()
