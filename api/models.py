from django.db import models

# Create your models here.


class Data(models.Model):
    store = models.ForeignKey('DataStore', on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    data = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.value


class DataStore(models.Model):
    name = models.CharField(max_length=200)
    value = models.ManyToManyField(Data, blank=True)

    def __str__(self):
        return self.name
