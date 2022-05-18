import os
#import time
import telegram.ext
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests

#import logging

from dotenv import load_dotenv

load_dotenv()

#logger = logging.getLogger()

#PRACTICUM_TOKEN = pass
# ключи доступа в .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=TELEGRAM_TOKEN)
# Обработка входящих сообщений
updater = Updater(token=TELEGRAM_TOKEN)

# ссылка на картинки
URL = 'https://api.thecatapi.com/v1/images/search'
NEWURL = 'https://api.thedogapi.com/v1/images/search'

# def parse_homework_status(homework):
#    homework_name = homework['homework_name']
#    status = homework['status']
#    if status not in ['rejected', 'approved']:
#        raise ValueError(f'пришел неожиданный статус: {status}')
#    elif status == 'rejected':
#        verdict = 'К сожалению в работе нашлись ошибки.'
#    elif status == 'approved':
#        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
#    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


#def get_homework_statuses(current_timestamp):
#    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
#    data = {
#        'from_date': current_timestamp
#    }
#    homework_statuses = requests.get(URL, headers=headers, params=data)
#    return homework_statuses.json()

# отправка соощений
#message='Фото котиков'


#def send_message(message):
#    return bot.send_message(chat_id=CHAT_ID, text=message)


#send_message(message)

# отправка фото
#URL = 'https://cdn2.thecatapi.com/images/3dl.jpg'
# Делаем GET-запрос к эндпоинту:
#response = requests.get(URL).json()
# Извлекаем из ответа URL картинки:
#random_cat_url = response[0].get('url')


#def send_photo(url):
#    return bot.send_photo(chat_id=CHAT_ID, photo=url)


#send_photo(random_cat_url)


#def main():
#    current_timestamp = int(time.time())  # начальное значение timestamp

#    while True:
#        try:
#            new_homework = get_homework_statuses(current_timestamp)
#            if new_homework.get('homeworks'):
#                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
#            if new_homework.get('current_date') is not None:
#                current_timestamp = new_homework.get('current_date')  # обновить timestamp
#            time.sleep(600)  # опрашивать раз в десять минут

#        except Exception as e:
#            print(f'Бот упал с ошибкой: {e}')
#            time.sleep(5)
#            continue


#if __name__ == '__main__':
#    send_message('Start Bot')
#    main()
# генератор случайных картинок
def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        print(error)
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(NEWURL)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


# отправка картинок в бот
def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение
    # будет отправлено 'Привет, я Olenchuk_Bot!'
    context.bot.send_message(chat_id=chat.id, text='Привет, я Olenchuk_Bot!')


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Посмотри, какого котика я тебе нашёл'
    chat = update.effective_chat
    # указал Имя пользователя
    name = update.message.chat.first_name
    # добавляем кнопку
    # Каждый вложенный список определяет
    # новый ряд кнопок в интерфейсе бота.
    # Здесь описаны две кнопки в первом ряду и одна - во втором.
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()


updater.dispatcher.add_handler(
    CommandHandler('start', wake_up)
)
updater.dispatcher.add_handler(
    CommandHandler('newcat', new_cat)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.text, say_hi)
)


updater.start_polling()
updater.idle()