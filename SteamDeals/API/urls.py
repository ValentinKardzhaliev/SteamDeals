from django.urls import path
from .views import top_selling_games

urlpatterns = [
    path('', top_selling_games, name='steam_apps'),
]
