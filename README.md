# Olenchuk_BOT
telegramm_bot

# как извлечь ссылку на картинки

```
import requests  # Импортируем библиотеку для работы с запросами
from telegram import Bot
bot = Bot(token='<token>')

# Адрес API сохраним в константе
URL = 'https://api.thecatapi.com/v1/images/search'  

# Сделаем GET-запрос к API
# метод json() преобразует полученный ответ JSON в тип данных, понятный Python
response = requests.get(URL).json()

# Рассмотрим структуру и содержимое переменной response
print(response)

# Посмотрим, какого типа переменная response
print(type(response))

# response - это список. А какой длины?
print(len(response))

# Посмотрим, какого типа первый элемент
print(type(response[0]))
```

## Вставляем в код
```
from telegram import Bot
import requests

bot = Bot(token='<token>')
URL = 'https://api.thecatapi.com/v1/images/search'
chat_id = <chat_id>

# Делаем GET-запрос к эндпоинту:
response = requests.get(URL).json()
# Извлекаем из ответа URL картинки:
random_cat_url = response[0].get('url')  

# Передаём chat_id и URL картинки в метод для отправки фото:
bot.send_photo(chat_id, random_cat_url) 
```
