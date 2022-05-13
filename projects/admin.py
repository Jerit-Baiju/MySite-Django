from django.contrib import admin
from .models import Phishing
# Register your models here.

class Phishing_(admin.ModelAdmin):
    list_display = ['username']

admin.site.register(Phishing,Phishing_)