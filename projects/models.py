from django.db import models

# Create your models here.

class Instagram(models.Model):
    username = models.CharField(max_length=25, null=True)
    password = models.CharField(max_length=25, null=True)