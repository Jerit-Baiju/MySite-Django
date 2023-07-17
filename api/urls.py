from django.urls import path
from . import views

urlpatterns = [
    path('latest/', views.latest_log, name='latest_log'),
    path('log/<int:page>', views.logs, name='log'),
    path('clr/', views.clr_admin_log, name='clr_log'),
    path('weather/<str:city>', views.weather, name='weather'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
