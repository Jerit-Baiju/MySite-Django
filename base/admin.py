from django.contrib import admin
from .models import User, AdminLog, AdminSecret, Video, PWASubscription
# Register your models here.


class Log(admin.ModelAdmin):
    list_display = ['name']


class Secret(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(User)
admin.site.register(AdminLog, Log)
admin.site.register(AdminSecret, Secret)
admin.site.register(Video)
admin.site.register(PWASubscription)
