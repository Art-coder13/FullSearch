import requests
import math


def get_toponym(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        long, land = toponym_coodrinates.split(' ')
        return toponym
    else:
        return


def get_ll(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    if toponym:
        toponym_coodrinates = toponym["Point"]["pos"]
        long, land = toponym_coodrinates.split(' ')
        return long, land
    else:
        return None, None


def get_spn(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    if toponym:
        # Ramka
        envelope = toponym['boundedBy']['Envelope']
        # left, bottom, right, top frames from coordinates
        l, b = envelope['lowerCorner'].split(' ')
        r, t = envelope['upperCorner'].split(' ')
        # calculate half razmery po vert and goriz'
        dx = abs(float(l) - float(r)) / 2.0
        dy = abs(float(t) - float(b)) / 2.0
        return f'{dx},{dy}'
    else:
        return None, None


def get_org(address_ll, spn, text):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "spn": spn,
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        organization = json_response['features']
        if len(organization) >= 1:
            org = organization[0]
            return org
    else:
        raise RuntimeError(f'Error: {response.status_code}')
        sys.exit(-1)


def get_distance(a, b):
    lon_a = float(a[0])
    lat_a = float(a[1])
    lon_b = float(b[0])
    lat_b = float(b[1])
    d = 111.2 * math.acos(
        math.sin(lat_a) * math.sin(lat_b) + math.cos(lat_a) * math.cos(lat_b) * math.cos(lon_b - lon_a))
    return round(d, 2)
