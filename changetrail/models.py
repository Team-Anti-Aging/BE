from django.db import models

# 사용자 모델
class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


# 관리자 모델
class Admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 산책로 모델
class WalkTrail(models.Model):
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    distance = models.CharField(max_length=20)
    route_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 산책로 경로 모델 (다중 경유지)
class Route(models.Model):
    trail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name='routes')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.trail.name} - ({self.latitude}, {self.longitude})"


# 민원 모델
class Feedback(models.Model):
    STATUS_CHOICES = [
        ('in_progress', '처리중'),
        ('completed', '완료'),
        ('rejected', '반려'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    walktrail = models.ForeignKey(WalkTrail, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    location = models.TextField()
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    feedback_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feedback_image = models.TextField(blank=True, null=True)  # URL or base64
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    response_content = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    response_image = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback #{self.id} by {self.user.nickname}"