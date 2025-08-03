from django.db import models

class WalkTrail(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=20)
    distance_km = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Route(models.Model):
    trail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.IntegerField()

    def __str__(self):
        return f"{self.name} - ({self.latitude}, {self.longitude})"
