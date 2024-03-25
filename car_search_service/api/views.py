from rest_framework import viewsets, status
from rest_framework.response import Response
from service.models import Location, Truck, Cargo
from .serializers import LocationSerializer, TruckSerializer, CargoSerializer
from rest_framework.decorators import action
from geopy.distance import geodesic


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def update(self, request, *args, **kwargs):
        truck = self.get_object()
        serializer = self.get_serializer(truck, data=request.data)
        if serializer.is_valid():
            zip_code = request.data.get('current_location', {}).get('zip_code')
            location = None
            if zip_code:
                location = Location.objects.get(zip_code=zip_code)
            truck.current_location = location
            truck.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cargo = serializer.save()
            self._update_nearby_trucks(cargo)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for cargo in queryset:
            self._update_nearby_trucks(cargo)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _update_nearby_trucks(self, cargo):
        trucks_within_radius = []
        for truck in Truck.objects.all():
            distance = geodesic((cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                                (truck.current_location.latitude, truck.current_location.longitude)).miles
            if distance <= 450:
                trucks_within_radius.append(truck.unique_number)
        cargo.nearby_trucks = trucks_within_radius
        cargo.save()

    @action(detail=True, methods=['patch'])
    def update_cargo(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(cargo, data=request.data, partial=True)
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