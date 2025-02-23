from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, SensorMeasurementViewSet

router = DefaultRouter()
router.register(r'systems', HydroponicSystemViewSet)
router.register(r'measurements', SensorMeasurementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
