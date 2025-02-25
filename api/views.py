from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import HydroponicSystem, SensorMeasurement
from .serializers import HydroponicSystemSerializer, SensorMeasurementSerializer, RegisterSerializer
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


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

    def get_object(self):
        """Retrieve object without filtering by user, then check permissions."""
        obj = get_object_or_404(HydroponicSystem, id=self.kwargs["pk"])  # Ensure object exists

        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this system.")  # Returns 403

        return obj


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

        - If `system_id` is provided, returns measurements for that system.
        - If no `system_id` is provided, returns all measurements from user's systems.
        - Returns an empty queryset if the request is from Swagger UI (`swagger_fake_view`).
        - Prevents errors when an AnonymousUser tries to access the data.
        """
        if getattr(self, 'swagger_fake_view', False):
            return SensorMeasurement.objects.none()

        if self.request.user.is_anonymous:
            return SensorMeasurement.objects.none()

        system_id = self.request.query_params.get('system_id')
        if not system_id:
            return SensorMeasurement.objects.filter(system__owner=self.request.user).order_by('-measured_at')

        hydro_system = get_object_or_404(HydroponicSystem, id=system_id, owner=self.request.user)
        return SensorMeasurement.objects.filter(system=hydro_system).order_by('-measured_at')

    def get_object(self):
        """Ensure users can only access or delete their own measurements."""
        obj = get_object_or_404(SensorMeasurement, id=self.kwargs["pk"])

        if obj.system.owner != self.request.user:  # Check ownership
            raise PermissionDenied("You do not have permission to access this measurement.")  # Return 403 Forbidden

        return obj  # Unauthorized users get 403

    def perform_create(self, serializer):
        """Ensure that pH validation errors result in 400 Bad Request instead of a server error."""
        try:
            instance = serializer.save()
            instance.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        response.data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response
