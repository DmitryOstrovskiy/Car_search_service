from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, CargoViewSet

router = DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'cargos', CargoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]