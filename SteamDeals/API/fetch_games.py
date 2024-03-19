from django.core.management.base import BaseCommand

from SteamDeals.API.models import Game
from SteamDeals.API.utils import fetch_games_by_concurrent_players, store_games_with_discount


class Command(BaseCommand):
    help = 'Fetches games by concurrent players and stores them with discounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching games by concurrent players...'))
        games_by_players = fetch_games_by_concurrent_players()

        # Delete existing data from the Game model
        Game.objects.all().delete()

        # Store new data
        store_games_with_discount(games_by_players)

        self.stdout.write(self.style.SUCCESS('Games fetched and stored successfully'))
