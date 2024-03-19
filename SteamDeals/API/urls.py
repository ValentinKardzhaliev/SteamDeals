from django.urls import path
from .views import fetch_and_store_games_with_discount

urlpatterns = [
    path('', fetch_and_store_games_with_discount, name='steam_apps'),
]
