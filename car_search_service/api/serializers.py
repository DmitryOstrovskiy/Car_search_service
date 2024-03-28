from rest_framework import serializers
from service.models import Location, Truck, Cargo
import random
from geopy.distance import geodesic


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('city', 'state', 'zip_code', 'latitude', 'longitude')


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ('unique_number', 'current_location', 'capacity')
        extra_kwargs = {'current_location': {'read_only': True}}

    def create(self, validated_data):
        locations = Location.objects.all()
        random_location = random.choice(locations) if locations else None
        truck = Truck.objects.create(
            unique_number=validated_data['unique_number'],
            capacity=validated_data['capacity'],
            current_location=random_location
        )
        return truck

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['current_location'] = LocationSerializer(
            instance.current_location).data
        return representation


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location_zip = serializers.CharField(write_only=True)
    delivery_location_zip = serializers.CharField(write_only=True)

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up_location_zip', 'delivery_location_zip',
                  'weight', 'description', 'nearby_trucks')

    def create(self, validated_data):
        pick_up_location_zip = validated_data.pop('pick_up_location_zip', None)
        delivery_location_zip = validated_data.pop('delivery_location_zip',
                                                   None)

        # Ищем локации с заданными zip-кодами
        try:
            pick_up_location = Location.objects.get(
                zip_code=pick_up_location_zip)
        except Location.DoesNotExist:
            raise serializers.ValidationError(
                {'pick_up_location_zip': 'Локации с таким ZIP не существует.'})

        try:
            delivery_location = Location.objects.get(
                zip_code=delivery_location_zip)
        except Location.DoesNotExist:
            raise serializers.ValidationError(
                {'delivery_location_zip': 'Локации с таким ZIP не существует.'})

        # Создаем груз с найденными локациями
        cargo = Cargo.objects.create(
            pick_up_location=pick_up_location,
            delivery_location=delivery_location,
            **validated_data
        )

        return cargo

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pick_up_location'] = LocationSerializer(
            instance.pick_up_location).data
        representation['delivery_location'] = LocationSerializer(
            instance.delivery_location).data
        return representation

    def update(self, instance, validated_data):
        pick_up_location_data = validated_data.get('pick_up_location')
        if pick_up_location_data:
            pick_up_location = instance.pick_up_location
            pick_up_location.city = pick_up_location_data.get(
                'city', pick_up_location.city)
            pick_up_location.state = pick_up_location_data.get(
                'state', pick_up_location.state)
            pick_up_location.zip_code = pick_up_location_data.get(
                'zip_code', pick_up_location.zip_code)
            pick_up_location.latitude = pick_up_location_data.get(
                'latitude', pick_up_location.latitude)
            pick_up_location.longitude = pick_up_location_data.get(
                'longitude', pick_up_location.longitude)
            pick_up_location.save()

        delivery_location_data = validated_data.get('delivery_location')
        if delivery_location_data:
            delivery_location = instance.delivery_location
            delivery_location.city = delivery_location_data.get(
                'city', delivery_location.city)
            delivery_location.state = delivery_location_data.get(
                'state', delivery_location.state)
            delivery_location.zip_code = delivery_location_data.get(
                'zip_code', delivery_location.zip_code)
            delivery_location.latitude = delivery_location_data.get(
                'latitude', delivery_location.latitude)
            delivery_location.longitude = delivery_location_data.get(
                'longitude', delivery_location.longitude)
            delivery_location.save()

        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        return instance


class CargoListSerializer(serializers.ModelSerializer):
    nearby_trucks_count = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up_location', 'delivery_location', 
                  'nearby_trucks_count')

    def get_nearby_trucks_count(self, obj):
        return len(obj.nearby_trucks)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pick_up_location'] = LocationSerializer(
            instance.pick_up_location).data
        representation['delivery_location'] = LocationSerializer(
            instance.delivery_location).data
        return representation


class TruckDistanceSerializer(serializers.Serializer):
    unique_number = serializers.CharField(read_only=True)
    distance = serializers.FloatField(read_only=True)


class CargoDetailSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    truck_distances = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up_location', 'delivery_location', 'weight',
                  'description', 'truck_distances')

    def get_truck_distances(self, obj):
        truck_distances = []
        cargo_location = (
            obj.pick_up_location.latitude,
            obj.pick_up_location.longitude) if obj.pick_up_location else None

        if cargo_location:
            for truck in Truck.objects.all():
                truck_location = (
                    truck.current_location.latitude,
                    truck.current_location.longitude)
                distance = geodesic(cargo_location, truck_location).miles
                if distance <= 450:  # Условие, чтобы включить только те грузовики, которые <= 450 миль
                    truck_distances.append({
                        'unique_number': truck.unique_number,
                        'distance': distance
                    })

        # Сортировка грузовиков по расстоянию
        truck_distances.sort(key=lambda x: x['distance'])

        # Возвращаем данные через 'TruckDistanceSerializer' для соответствия формату
        return TruckDistanceSerializer(truck_distances, many=True).data


class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('weight', 'description')

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance
