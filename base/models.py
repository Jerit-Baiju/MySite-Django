from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(unique=True, max_length=200, null=True)
    email = models.EmailField(max_length=200)
    log = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.name} - {self.username}"


class AdminLog(models.Model):
    name = models.CharField(max_length=40, null=True)
    latest_log = models.CharField(max_length=250, null=True, blank=True)
    log = models.TextField(null=True, blank=True)


class AdminSecret(models.Model):
    name = models.CharField(max_length=20, null=True)
    secret = models.CharField(max_length=100, null=True, blank=True)
