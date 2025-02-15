import requests


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
