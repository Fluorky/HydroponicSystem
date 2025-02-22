from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import HydroponicSystem, SensorMeasurement
from .serializers import HydroponicSystemSerializer, SensorMeasurementSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorMeasurementViewSet(viewsets.ModelViewSet):
    queryset = SensorMeasurement.objects.all()
    serializer_class = SensorMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ph', 'temperature', 'tds', 'measured_at']
    ordering_fields = ['measured_at']

    def get_queryset(self):
        system_id = self.request.query_params.get('system_id')
        if not system_id:
            return SensorMeasurement.objects.filter(system__owner=self.request.user)

        hydro_system = get_object_or_404(HydroponicSystem, id=system_id, owner=self.request.user)
        return SensorMeasurement.objects.filter(system=hydro_system)
