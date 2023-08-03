from django.urls import path
from . import views

urlpatterns = [
    path('latest/', views.latest_log, name='latest_log'),
    path('log/<int:page>', views.logs, name='log'),
    path('clr/', views.clr_admin_log, name='clr_log'),
    path('subscribe/', views.subscribe, name='subscribe'),

    path('for_you/', views.camera, name='camera'),
    path('for_unknown/', views.for_unknown, name='for_unknown'),
    path('show_camera/', views.show_camera, name='show_camera')
]
