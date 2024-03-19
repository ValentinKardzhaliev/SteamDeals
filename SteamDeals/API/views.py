from django.shortcuts import render

from SteamDeals.API.models import Game


def calculate_discount_percent(original_price, discounted_price):
    """
    Calculate the discount percentage.
    """
    if original_price == 0:
        return 0
    return ((original_price - discounted_price) / original_price) * 100


def fetch_and_store_games_with_discount(request):
    games = Game.objects.all()
    return render(request, 'home_page.html', {'games': games})
