from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import HydroponicSystem, SensorMeasurement
from .serializers import HydroponicSystemSerializer, SensorMeasurementSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for API views.

    - Default page size: 10
    - Allows user to specify page size (max: 100)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing hydroponic systems.

    - Supports CRUD operations (Create, Read, Update, Delete)
    - Restricts access to authenticated users
    - Ensures users can only access their own hydroponic systems
    - Provides ordering by name and creation date
    """
    queryset = HydroponicSystem.objects.all()  # Required for automatic basename detection
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        """
        Return only hydroponic systems belonging to the authenticated user.

        - Returns an empty queryset if the request is from Swagger UI (`swagger_fake_view`).
        - Prevents errors when an AnonymousUser tries to access the data.
        """
        if getattr(self, 'swagger_fake_view', False):  # Schema generation case
            return HydroponicSystem.objects.none()

        if self.request.user.is_anonymous:
            return HydroponicSystem.objects.none()

        return HydroponicSystem.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Ensure that the hydroponic system is associated with the logged-in user."""
        serializer.save(owner=self.request.user)


class SensorMeasurementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sensor measurements.

    - Supports CRUD operations
    - Restricts access to authenticated users
    - Filters by pH, temperature, TDS, and measurement date
    - Provides ordering by measurement date
    """
    queryset = SensorMeasurement.objects.all()  # Required for automatic basename detection
    serializer_class = SensorMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ph', 'temperature', 'tds', 'measured_at']
    ordering_fields = ['measured_at']

    def get_queryset(self):
        """
        Return sensor measurements for a specific hydroponic system owned by the user.

        - Returns an empty queryset if the request is from Swagger UI (`swagger_fake_view`).
        - Prevents errors when an AnonymousUser tries to access the data.
        """
        if getattr(self, 'swagger_fake_view', False):  # Schema generation case
            return SensorMeasurement.objects.none()

        if self.request.user.is_anonymous:
            return SensorMeasurement.objects.none()

        system_id = self.request.query_params.get('system_id')
        if not system_id:
            return SensorMeasurement.objects.filter(system__owner=self.request.user).order_by('-measured_at')

        hydro_system = get_object_or_404(HydroponicSystem, id=system_id, owner=self.request.user)
        return SensorMeasurement.objects.filter(system=hydro_system).order_by('-measured_at')
