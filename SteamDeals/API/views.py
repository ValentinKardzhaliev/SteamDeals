import requests
from django.shortcuts import render


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


def get_games_by_concurrent_players():
    url = "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        games = data.get("response", {}).get("ranks", [])[:5]

        formatted_games = []
        for game in games:
            appid = game.get('appid')
            concurrent_in_game = game.get('concurrent_in_game')
            peak_in_game = game.get('peak_in_game')
            formatted_games.append(
                {'appid': appid, 'concurrent_in_game': concurrent_in_game, 'peak_in_game': peak_in_game})

        return formatted_games
    except requests.RequestException as e:
        print(f"Error fetching games by concurrent players: {e}")
        return []



def get_app_price(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get(str(app_id), {}).get('success', False):
            is_free = data[str(app_id)].get('data', {}).get('is_free', False)
            if is_free:
                return 'Free'

            price_data = data[str(app_id)].get('data', {}).get('price_overview', {})
            return price_data.get('final_formatted', 'Price not available')
        else:
            return 'Price not available'
    except requests.RequestException as e:
        return str(e)


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


def top_selling_games(request):
    games_by_players = get_games_by_concurrent_players()
    top_selling_apps = []

    for game in games_by_players:
        app_id = game.get('appid')
        name = get_app_name(app_id)
        price = get_app_price(app_id)
        image_url = get_app_image_url(app_id)

        if name and price and image_url:
            top_selling_apps.append({
                'name': name,
                'price': price,
                'image_url': image_url
            })

    return render(request, 'home_page.html', {'top_selling_apps': top_selling_apps})