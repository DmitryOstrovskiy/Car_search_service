import csv
from django.core.management.base import BaseCommand
from service.models import Location

class Command(BaseCommand):
    help = 'Загрузка списка локаций из CSV-файла в базу данных'

    def handle(self, *args, **kwargs):
        with open('data/uszips.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                location, created = Location.objects.get_or_create(
                    zip_code=row['zip'],
                    defaults={
                        'latitude': row['lat'],
                        'longitude': row['lng'],
                        'city': row['city'],
                        'state': row['state_name']
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Location {row['zip']} added.")
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(f"Location {row['zip']} already exists.")
                    )
