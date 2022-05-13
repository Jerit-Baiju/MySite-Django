from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('clara/', views.clara, name='clara'),
    path('sadance/', views.sadance, name='sadance'),
    path('num_game/', views.num_Game, name='num-game'),
    path('num_game_add/', views.num_Game_add, name='num-game-add'),
    path('weather/', views.weather, name='weather'),
]
