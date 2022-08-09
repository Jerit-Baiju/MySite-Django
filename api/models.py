from django.db import models

# Create your models here.

class Data(models.Model):
    value = models.CharField(max_length=200)
    data = models.TextField(null=True, blank=True)


class DataStore(models.Model):
    name = models.CharField(max_length=200)
    data = models.ManyToManyField(Data, blank=True)