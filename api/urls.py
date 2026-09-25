from django.urls import path
from . import views

urlpatterns = [
    path('latest/', views.latest_log, name='latest_log'),
    path('log/<int:page>', views.logs, name='log'),
    path('clr/', views.clr_admin_log, name='clr_log'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('upload/', views.upload_image),
    path('nlp/', views.nlp_list, name='nlp_list'),
    path('nlp', views.nlp_list, name='nlp_list_noslash'),
    path('nlp/py/', views.nlp_py, name='nlp_py'),
    path('nlp/py', views.nlp_py, name='nlp_py_noslash'),
    path('nlp/<str:pid>', views.nlp_code, name='nlp_code'),
    path('nlp/<str:pid>/', views.nlp_code, name='nlp_code_slash'),
]
