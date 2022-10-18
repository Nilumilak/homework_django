from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
