from django.db import models

from django.db import models

class WalkTrail(models.Model):
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    distance = models.CharField(max_length=20)
    route_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    trail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name='routes')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.trail.name} - ({self.latitude}, {self.longitude})"
