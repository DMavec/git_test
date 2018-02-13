from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:player_name>/', views.player_stats, name='player_stats')
]