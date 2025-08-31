from django.db import models

# Create your models here.

class WeatherData(models.Model):
    wind_speed = models.FloatField()   # km/h
    rainfall = models.FloatField()     # mm
    tide_level = models.FloatField()   # meters
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} | Wind: {self.wind_speed} km/h"
    
class Alert(models.Model):
    LEVEL_CHOICES = [
        ('GREEN', 'Safe'),
        ('YELLOW', 'Be Alert'),
        ('ORANGE', 'Prepare'),
        ('RED', 'Danger'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

