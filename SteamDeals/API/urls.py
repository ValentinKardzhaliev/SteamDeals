from django.urls import path
from .views import random_apps_with_price_and_names

urlpatterns = [
    path('steam-apps/', random_apps_with_price_and_names, name='steam_apps'),
]
