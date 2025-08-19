from django.db import models
from accounts.models import User
from feedback.models import Feedback
from walktrails.models import WalkTrail


# Create your models here.
class Response(models.Model):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(max_length=20, choices=Feedback.STATUS_CHOICES, default='in_progress')
    response_content = models.TextField(blank=True, null=True)
    response_image_url = models.URLField(blank=True, null=True)
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to Feedback #{self.feedback} by {self.admin.nickname}" if self.admin else "Response without Admin"

class AIReport(models.Model):
    walktrail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name="ai_reports")
    report_text = models.TextField()  # GPT가 생성한 전체 리포트
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)