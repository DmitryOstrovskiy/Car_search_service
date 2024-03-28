from rest_framework import viewsets, status
from rest_framework.response import Response
from service.models import Location, Truck, Cargo
from .serializers import (LocationSerializer, TruckSerializer, CargoSerializer,
                          CargoListSerializer, CargoDetailSerializer,
                          CargoUpdateSerializer)
from rest_framework.decorators import action
from geopy.distance import geodesic
from django_filters.rest_framework import DjangoFilterBackend


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def update(self, request, *args, **kwargs):
        truck = self.get_object()
        # Получаем новый zip-код из запроса
        zip_code = request.data.get('zip_code')
        # Обновляем только поле current_location
        if zip_code:
            try:
                location = Location.objects.get(zip_code=zip_code)
                truck.current_location = location
                truck.save()
            except Location.DoesNotExist:
                return Response(
                    {"error": "Локации с указанным zip не существует."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Сериализуем обновленную машину для ответа
        serializer = self.get_serializer(truck)
        return Response(serializer.data)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['weight']

    def get_serializer_class(self):
        if self.action == 'list':
            return CargoListSerializer
        elif self.action == 'retrieve':
            return CargoDetailSerializer
        elif self.action == 'update':
            return CargoUpdateSerializer
        else:
            return CargoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cargo = serializer.save()
            self._update_nearby_trucks(cargo)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Извлекаем параметры запроса
        weight = request.query_params.get('weight')
        miles = request.query_params.get('miles')

        queryset = self.filter_queryset(self.get_queryset())

        if weight is not None:
            queryset = queryset.filter(weight=weight)

        if miles is not None:
            miles = float(miles)
            new_queryset = []
            for cargo in queryset:
                self._update_nearby_trucks(cargo)
                if len(cargo.nearby_trucks) > 0:
                    nearest_truck_miles = min([geodesic(
                        (cargo.pick_up_location.latitude,
                         cargo.pick_up_location.longitude),
                        (Truck.objects.get(
                            unique_number=truck_number
                            ).current_location.latitude,
                         Truck.objects.get(
                             unique_number=truck_number
                             ).current_location.longitude)
                    ).miles for truck_number in cargo.nearby_trucks])
                    if nearest_truck_miles <= miles:
                        new_queryset.append(cargo)
            queryset = new_queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def _update_nearby_trucks(self, cargo):
        trucks_within_radius = []
        for truck in Truck.objects.all():
            distance = geodesic((cargo.pick_up_location.latitude,
                                 cargo.pick_up_location.longitude),
                                (truck.current_location.latitude,
                                 truck.current_location.longitude)).miles
            if distance <= 450:
                trucks_within_radius.append(truck.unique_number)
        cargo.nearby_trucks = trucks_within_radius
        cargo.save()

    @action(detail=True, methods=['patch'])
    def update_cargo(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(cargo, data=request.data,
                                         partial=True)
        if serializer.is_valid():
            cargo = serializer.save()
            self._update_nearby_trucks(cargo)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        cargo = self.get_object()
        self.perform_destroy(cargo)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
