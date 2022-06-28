import os
import requests as requests

yandex_token = os.getenv('YANDEX_SHEDULE')
url = 'https://api.rasp.yandex.net/v3.0/search/'
headers = {'Authorization': f'OAuth {yandex_token}'}
# From - Код станции отправления. Должен быть указан в системе кодирования.
# To - Код станции прибытия. Должен быть указан в системе кодирования.
# date - Дата, на которую необходимо получить список рейсов.
# Должна быть указана в формате, соответствующем стандарту ISO 8601. Например, YYYY-MM-DD.
# transport_types - Тип транспортного средства. Возможные значения:
# plane — самолет;
# train — поезд;
# suburban — электричка;
# bus — автобус;
# water — морской транспорт;
# helicopter — вертолет.
station_from = 's9603624' # Левашово
station_to = 's9603463' # Удельная
date = '2022-05-19'
transport_types = 'suburban' # электричка
payload = {'from': {station_from},
           'to': {station_to},
           'date': {date},
            'transport_types': {transport_types}
}

# Делаем GET-запрос к эндпоинту url с заголовком headers и параметрами params
homework_statuses = requests.get(url, headers=headers, params=payload)

# Печатаем ответ API в формате JSON
print(homework_statuses.text)

# А можно ответ в формате JSON привести к типам данных Python и напечатать и его
# print(homework_statuses.json())