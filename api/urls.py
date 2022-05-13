from django.urls import path
from . import views

urlpatterns = [
    path(f'latest/', views.latest_log, name='latest_log'),
    path(f'log/', views.log, name='log'),
    path(f'clr/', views.clr_admin_log, name='clr_log')
]
