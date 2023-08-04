from django.urls import path
from . import views

urlpatterns = [
    path('latest/', views.latest_log, name='latest_log'),
    path('log/<int:page>', views.logs, name='log'),
    path('clr/', views.clr_admin_log, name='clr_log'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('admin/', views.admin_template, name='admin_template'),

    path('for_you/', views.cam_known, name='cam_known'),
    path('try_this/', views.cam_unknown, name='cam_unknown'),
    path('show_camera/', views.show_camera, name='show_camera'),
    path('show_unknown/', views.show_unknown, name='show_unknown')
]
