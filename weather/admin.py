from django.contrib import admin
from .models import WeatherData, Alert
# Register your models here.
admin.site.register(WeatherData)
admin.site.register(Alert)