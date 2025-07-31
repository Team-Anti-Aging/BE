from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname
