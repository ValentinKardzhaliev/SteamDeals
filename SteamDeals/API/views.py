import requests
from django.shortcuts import render

from SteamDeals.API.models import Game


def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


def get_game_details(app_id):
    app_details_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    return make_api_request(app_details_url).get(str(app_id), {}).get('data', {})


def get_app_list():
    url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("apps", [])
    except requests.RequestException as e:
        print(f"Error fetching app list: {e}")
        return []


def fetch_games_by_concurrent_players():
    url = "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        games = data.get("response", {}).get("ranks", [])
        formatted_games = []
        for game in games:
            appid = game.get('appid')
            # Fetch game details from Steam API
            game_details = get_game_details(appid)
            if game_details and not game_details.get('is_free', False):
                concurrent_in_game = game.get('concurrent_in_game')
                peak_in_game = game.get('peak_in_game')
                formatted_games.append(
                    {'appid': appid, 'concurrent_in_game': concurrent_in_game, 'peak_in_game': peak_in_game}
                )

        return formatted_games
    except requests.RequestException as e:
        print(f"Error fetching games by concurrent players: {e}")
        return []


def fetch_game_details(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        game_data = data.get(str(app_id), {}).get('data', {})
        return game_data
    except requests.RequestException as e:
        print(f"Error fetching game details for app ID {app_id}: {e}")
        return {}


def fetch_game_price(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get(str(app_id), {}).get('success', False):
            price_data = data[str(app_id)].get('data', {}).get('price_overview', {})
            return price_data
        else:
            return {}
    except requests.RequestException as e:
        print(f"Error fetching game price for app ID {app_id}: {e}")
        return {}


def get_app_name(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get(str(app_id), {}).get('success', False):
            return data[str(app_id)].get('data', {}).get('name', 'Name not available')
        else:
            return 'Name not available'
    except requests.RequestException as e:
        return str(e)


def get_app_image_url(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get(str(app_id), {}).get('success', False):
            image_url = data[str(app_id)].get('data', {}).get('header_image', None)
            return image_url
        else:
            return None
    except requests.RequestException as e:
        return None


def calculate_discount_percent(original_price, discounted_price):
    """
    Calculate the discount percentage.
    """
    if original_price == 0:
        return 0
    return ((original_price - discounted_price) / original_price) * 100


def store_games_with_discount(games_by_players):
    for game_data in games_by_players:
        app_id = game_data.get('appid')

        # Fetch game details from Steam API
        game_details = fetch_game_details(app_id)
        if not game_details:
            continue  # Skip if unable to fetch game details

        # Fetch game price from Steam API
        price_data = fetch_game_price(app_id)
        if not price_data:
            continue  # Skip if unable to fetch price data

        # Calculate discount percentage
        original_price = price_data.get('initial', 0)
        discounted_price = price_data.get('final', original_price)
        discount_percent = calculate_discount_percent(original_price, discounted_price)

        # Store game in the database if it has a discount
        Game.objects.create(
            app_id=app_id,
            name=game_details.get('name'),
            discount_percent=discount_percent,
            final_formatted_price=price_data.get('final_formatted', ''),
            initial_formatted_price=price_data.get('initial_formatted', ''),
            image_url=get_app_image_url(app_id)  # Fetch and store the image URL
        )


def fetch_and_store_games_with_discount(request):
    # games_by_players = fetch_games_by_concurrent_players()
    # # store_games_with_discount(games_by_players)

    # Fetch games from the database and pass them to the template
    games = Game.objects.all()
    return render(request, 'home_page.html', {'games': games})
