from django.contrib import admin
from .models import Instagram
# Register your models here.

class Instagram_(admin.ModelAdmin):
    list_display = ['username']

admin.site.register(Instagram,Instagram_)