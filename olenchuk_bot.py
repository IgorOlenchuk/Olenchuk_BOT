import os
#import time
import telegram.ext
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, MessageFilter
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import requests

import logging

import validators

import whois

import time

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


#PRACTICUM_TOKEN = pass
# ключи доступа в .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=TELEGRAM_TOKEN)
# Обработка входящих сообщений
updater = Updater(token=TELEGRAM_TOKEN)

#настраиваем браузер для корректной работы в headless режиме
binary = FirefoxBinary('/bin/firefox')
browser = webdriver.Firefox()
browser = FirefoxOptions()
browser.add_argument('--headless')
browser.add_argument('--disable-gpu')
browser.add_argument('--disable-dev-shm-usage')
browser.add_argument('--no-sandbox')


# ссылка на картинки
URL = 'https://api.thecatapi.com/v1/images/search'
# 'https://api.thecatapi.com/v1/images/search'
NEWURL = 'https://api.thedogapi.com/v1/images/search'

# генератор случайных картинок
def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

# отправка картинок в бот
def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

# обработка скриншотов
def get_screenshot(update, context):
    chat = update.effective_chat
    url = ""
    try:
        url = update.message.text
    except IndexError:
        context.bot.send_message(chat_id=chat.id, text='You have not entered URL!')
        return
    if not validators.url(url):
        context.bot.send_message(chat_id=chat.id, text='URL is invalid!')
    else:
        tic = time.perf_counter()
        context.bot.send_message(chat_id=chat.id,  text='Подождите, информация загружается...')
        photo_path = str(chat.id) + '.png'
        browser = webdriver.Firefox()
        browser.set_window_size(1280, 720)
        browser.get(url)
        browser.save_screenshot(photo_path)
        browser.quit()
        whois_info = whois.whois(url)
        toc = time.perf_counter()
        context.bot.send_photo(chat_id=chat.id, photo = open(photo_path, 'rb'), caption=f"{whois_info.domain_name}, Веб-сайт: {url} Время обработки: {toc - tic:0.4f} секунды")
        context.bot.send_message(chat.id, text=f"{whois_info.domain_name}")


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение
    # будет отправлено 'Привет, я Olenchuk_Bot!'
    context.bot.send_message(chat_id=chat.id, text='Привет, я Olenchuk_Bot!')


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Привет,  {}! Меня зовут Olencuhk_Imager.'
    chat = update.effective_chat
    # указал Имя пользователя
    name = update.message.chat.first_name
    # добавляем кнопки
    # Каждый вложенный список определяет
    # новый ряд кнопок в интерфейсе бота.
    # Здесь описаны две кнопки в первом ряду и одна - во втором.
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['Добавить Olenchuk_Imager в свой чат'], ['Выбор языка']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет,  {}! Меня зовут Olencuhk_Imager.'
             'Я - Бот для создания веб-скриншотов.'
             'Чтобы получить скриншот - отправьте URL адрес сайта. Например, https://wikipedia.org'
             '• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)'
             '• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.'
             ' Olencuhk_Imager. использует chromedriver.'
             'Работает с протоколами http, https.'
             'И находится в постоянной разработке.'
             .format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())

# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()

class FilterUrl(MessageFilter):
    def filter(self, message):
        return '.' in message.text

my_filter = FilterUrl()


def main():
    updater.dispatcher.add_handler(
        CommandHandler('start', wake_up)
    )
    updater.dispatcher.add_handler(
        MessageHandler(my_filter, get_screenshot)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Добавить Olenchuk_Imager в свой чат'), new_cat)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text('Выбор языка'), wake_up)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, say_hi)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
