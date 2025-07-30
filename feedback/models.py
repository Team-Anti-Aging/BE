from django.db import models

from django.db import models
from accounts.models import User, Admin
from walktrails.models import WalkTrail

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('in_progress', '처리중'),
        ('completed', '완료'),
        ('rejected', '반려'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    walktrail = models.ForeignKey(WalkTrail, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    location = models.TextField()
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    feedback_content = models.TextField()
    feedback_image = models.TextField(blank=True, null=True)  # URL 또는 base64
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 응답 관련 필드
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    response_content = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    response_image = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback #{self.id} by {self.user.nickname}"
