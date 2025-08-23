from django.db import models
from accounts.models import User
from walktrails.models import WalkTrail

# Create your models here.
class Favorite_walktrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_by')
    walktrail = models.ForeignKey(WalkTrail, on_delete=models.CASCADE, related_name='favorite_policy')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 중복방지
        constraints = [models.UniqueConstraint(fields=['user', 'walktrail'], name='uniq_user_walktrail')]