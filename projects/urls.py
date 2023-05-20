from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('clara/', views.clara, name='clara'),
    path('num_game/', views.num_game, name='num-game'),
    path('num_game_add/', views.num_game_add, name='num-game-add'),
]
