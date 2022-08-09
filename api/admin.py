from django.contrib import admin
from .models import DataStore, Data

# Register your models here.

admin.site.register(DataStore)
admin.site.register(Data)
