from rest_framework import serializers
from .models import HydroponicSystem, SensorMeasurement


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = '__all__'
        read_only_fields = ['owner']


class SensorMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorMeasurement
        fields = '__all__'
        read_only_fields = ['measured_at']
