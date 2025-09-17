from django.db import models
from django.utils import timezone

class WeatherRecord(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C on {self.date.strftime('%Y-%m-%d')}"


