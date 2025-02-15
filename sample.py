import requests
from geocoder import get_ll, get_spn
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
# toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = 'Москва, ул. Ак. Королева, 12'

# Долгота и широта:
toponym_longitude, toponym_lattitude = get_ll(toponym_to_find)

delta = get_spn(toponym_to_find)
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": delta,
    "apikey": apikey,
    'pt': ",".join([toponym_longitude, toponym_lattitude])

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
