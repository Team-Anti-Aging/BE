from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


class Admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
