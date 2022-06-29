import os
import logging
from aiogram import Bot, types, filters
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, ChatActions

import keyboards as kb

from dotenv import load_dotenv

import validators

import whois

import time

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

binary = FirefoxBinary('/bin/firefox')

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    text = 'Привет! Меня зовут Olencuhk_Imager.\n' \
          'Я - Бот для создания веб-скриншотов.\n' \
          'Чтобы получить скриншот - отправьте URL адрес сайта. Например, https://wikipedia.org.\n' \
          '• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)\n' \
          '• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.\n' \
          'Olencuhk_Imager. использует chromedriver.\n' \
          'Работает с протоколами https.\n' \
          'И находится в постоянной разработке.\n'
    await msg.answer(text=text, reply_markup=kb.inline_kb_full)


@dp.message_handler()
async def get_screenshot(msg: types.Message):
    url = ""
    try:
        uid = msg.chat.id
        url = msg.text
    except IndexError:
        await msg.answer('Вы не ввели адрес сайта!')
        return
    if not validators.url(f'https://{url}'):
        await msg.answer('Ошибка в адресе сайта')
    else:
        tic = time.perf_counter()
        msg  = await msg.answer('Подождите, информация загружается...')
        photo_path = str(uid) + '.png'
        browser = webdriver.Firefox()
        browser.set_window_size(1280, 720)
        browser.get(f'https://{url}')
        browser.save_screenshot(photo_path)
        browser.quit()
        whois_info = whois.whois(url)
        toc = time.perf_counter()
        await bot.send_photo(msg.chat.id,
                             photo = open(photo_path, 'rb'),
                             caption=f"{whois_info.domain_name}, Веб-сайт: {url} Время обработки: {toc - tic:0.4f} секунды",
                             reply_markup=kb.inline_kb_3)
        await msg.delete()
        


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)



if __name__ == '__main__':
    executor.start_polling(dp)