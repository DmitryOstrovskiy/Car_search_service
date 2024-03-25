from django.db import models
from django.contrib.postgres.fields import ArrayField
from api.validators import validate_unique_number
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = ('city', 'state', 'zip_code')

    def str(self):
        return f'{self.city}, {self.state}, {self.zip_code}'

class Truck(models.Model):
    unique_number = models.CharField(max_length=5, unique=True, validators=[validate_unique_number])
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField(validators=[
        MinValueValidator(
            1, message='Минимальная грузоподъемность не может быть менее 1'),
            MaxValueValidator(
                1000, message='Максимальная грузоподъемность не может быть более 1000')])

    def str(self):
        return self.unique_number

class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, related_name='pick_up_location', on_delete=models.SET_NULL, null=True)
    delivery_location = models.ForeignKey(Location, related_name='delivery_location', on_delete=models.SET_NULL, null=True)
    weight = models.PositiveIntegerField(validators=[
        MinValueValidator(
            1, message='Минимальная грузоподъемность не может быть менее 1'),
            MaxValueValidator(
                1000, message='Максимальная грузоподъемность не может быть более 1000')])
    description = models.TextField()
    nearby_trucks = ArrayField(models.CharField(max_length=5), default=list)

    def str(self):
        return f'Cargo ID: {self.id}'