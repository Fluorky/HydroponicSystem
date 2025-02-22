from django.contrib.auth.models import User
from django.db import models


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SensorMeasurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='measurements')
    ph = models.FloatField()
    temperature = models.FloatField()
    tds = models.FloatField()
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"pH: {self.ph}, Temp: {self.temperature}, TDS: {self.tds}"
