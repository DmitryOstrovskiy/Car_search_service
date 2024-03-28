import random
from django.core.management.base import BaseCommand
from service.models import Truck, Location
from django.core.exceptions import ValidationError
import string


class Command(BaseCommand):
    help = 'Создайте 20 грузовиков со случайным назначением локации'

    def add_arguments(self, parser):
        # Named (optional) argument
        parser.add_argument('--number', type=int, help='Укажите количество грузовых автомобилей для создания', default=20)

    def handle(self, *args, **options):
        locations = list(Location.objects.all())
        if not locations:
            raise ValidationError("Локации не найдены. Пожалуйста, сначала загрузите локации.")

        count = options['number']
        for _ in range(count):
            unique_number = self._generate_unique_number()
            current_location = random.choice(locations)
            capacity = random.randint(1, 1000)

            Truck.objects.create(
                unique_number=unique_number,
                current_location=current_location,
                capacity=capacity
            )
            self.stdout.write(self.style.SUCCESS(f'Грузовик {unique_number} создан с указанием локации {current_location}'))

    def _generate_unique_number(self):
        while True:
            number = random.randint(1000, 9999)
            letter = random.choice(string.ascii_uppercase)
            unique_number = f"{number}{letter}"
            if not Truck.objects.filter(unique_number=unique_number).exists():
                return unique_number
