from django.contrib import admin
from .models import HydroponicSystem, SensorMeasurement


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)


@admin.register(SensorMeasurement)
class SensorMeasurementAdmin(admin.ModelAdmin):
    list_display = ('system', 'ph', 'temperature', 'tds', 'measured_at')
    search_fields = ('system__name',)
    list_filter = ('measured_at', 'ph', 'temperature', 'tds')
