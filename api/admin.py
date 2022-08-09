from django.contrib import admin
from .models import DataStore, Data

# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ['key', 'data']
    list_filter = ['store']
    ordering = ['key']


admin.site.register(DataStore)
admin.site.register(Data, DataAdmin) 
