from django.contrib import admin
from .models import DataStore, Data

# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ['store','key', 'data']
    ordering = ['store','key']


admin.site.register(DataStore)
admin.site.register(Data, DataAdmin) 
