from django.http import JsonResponse
import requests
import random


def get_app_price(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get(str(app_id), {}).get('success', False):
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


def random_apps_with_price_and_names(request):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        apps = data.get("applist", {}).get("apps", [])
        random_apps = random.sample(apps, min(3, len(apps)))
        apps_with_price_and_names = []
        for app in random_apps:
            app_id = app.get('appid')
            name = get_app_name(app_id)
            price = get_app_price(app_id)
            apps_with_price_and_names.append({'appid': app_id, 'name': name, 'price': price})
        return JsonResponse(apps_with_price_and_names, safe=False)
    else:
        return JsonResponse([], safe=False)
