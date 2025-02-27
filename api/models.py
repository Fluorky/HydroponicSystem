from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SensorMeasurement(models.Model):
    system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
    )
    ph = models.FloatField()
    temperature = models.FloatField()
    tds = models.FloatField()
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"pH: {self.ph}, Temp: {self.temperature}, TDS: {self.tds}"

    def clean(self):
        """Ensure that the pH value is within a valid range (0-14)."""
        if not (0 <= self.ph <= 14):
            raise ValidationError({"ph": "pH value must be between 0 and 14."})

    def save(self, *args, **kwargs):
        """Run model validation before saving."""
        self.full_clean()  # This ensures model validation runs before saving
        super().save(*args, **kwargs)
