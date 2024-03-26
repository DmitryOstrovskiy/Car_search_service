from celery import shared_task
from service.models import Truck, Location
import random
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def update_truck_locations():
    logger.info("Starting the update of truck locations...")
    locations = list(Location.objects.all())
    for truck in Truck.objects.all():
        new_location = random.choice(locations) if locations else None
        if new_location:
            truck.current_location = new_location
            truck.save()
    logger.info("Finished updating truck locations.")
