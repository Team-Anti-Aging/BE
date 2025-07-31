from django.db import models

from django.db import models
from accounts.models import User
from walktrails.models import WalkTrail

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('in_progress', '처리중'),
        ('completed', '완료'),
        ('rejected', '반려'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    walktrail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name='feedback')
    location = models.TextField()
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    feedback_content = models.TextField()
    feedback_image = models.TextField(blank=True, null=True)  # URL 또는 base64
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"Feedback by {self.user.nickname}"



    
