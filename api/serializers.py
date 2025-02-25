from django.contrib.auth.models import User
from rest_framework import serializers
from .models import HydroponicSystem, SensorMeasurement


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_name(self, value):
        """Ensure each user cannot create a system with the same name twice."""
        user = self.context['request'].user
        if HydroponicSystem.objects.filter(owner=user, name=value).exists():
            raise serializers.ValidationError("You already have a system with this name.")
        return value


class SensorMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorMeasurement
        fields = '__all__'
        read_only_fields = ['measured_at']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
