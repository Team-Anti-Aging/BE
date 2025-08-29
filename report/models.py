from django.db import models
from accounts.models import User

# Create your models here.
class Custom_ai_report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report')
    title = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    instruction = models.TextField()
    docs_id = models.ManyToManyField("feedback.Feedback", related_name="report")
    report = models.TextField(null = True, blank=True)