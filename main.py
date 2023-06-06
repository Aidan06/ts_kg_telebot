from dotenv import load_dotenv
import os
import requests
import telebot
from telebot import types

from bs4 import BeautifulSoup
from news import get_days_series_from_site


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

choices = [
    {
        'name': 'Новости за день',
        'site': 'https://www.ts.kg/news'
    },
    {
        'name': 'Самостоятельный поиск',
        'site': 'https://www.ts.kg/search'
    },
    {
        'name': 'Перейти на сайт',
        'site': 'https://www.ts.kg'
    },
]

news_days = []
news_day_id = []
series_in_a_day = []
tv_series = []


@bot.message_handler(commands=['start'])
def get_tvseries(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    news_button = types.KeyboardButton('Новости')
    search_button = types.KeyboardButton('Поиск вручную')
    website_button = types.KeyboardButton('Сразу перейти на сайт')
    markup.row(*[choice.get('name') for choice in choices])
    bot.send_message(message.chat.id, 'Привет! Что бы вы хотели сделать?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_days_series(message):
    if message.text == choices[0]['name']:
        get_days_series_from_site(news_days, choices[0]['site'])

        markup = types.InlineKeyboardMarkup()
        for news_day in news_days:
            news_day_id.append(news_day.get('id'))
            button = types.InlineKeyboardButton(news_day.get('name'),
                                                callback_data=news_day.get('id'))
            markup.add(button)

        bot.send_message(message.chat.id, 'Даты новостей ', reply_markup=markup)

    elif message.text == choices[1]['name']:
        pass
    elif message.text == choices[2]['name']:
        pass
    else:
        bot.send_message(message.chat.id, 'Сделайте выбор!')


@bot.callback_query_handler(lambda query: query.data in news_day_id)
def callback_news_day_series(query):
    news_day_id = query.data.split('.')[0]
    for news_day in news_days:
        if news_day.get('id') == news_day_id:
            url = f'{choices[0].get("site")}{choices.get("url")}'
            series_in_a_day(tv_series, url)

            for tv_serial in tv_series:
                 bot.send_message(query.from_user.id, tv_serial.get('name'))


@bot.message_handler(func=lambda message: message.text == 'Сразу перейти на сайт')
def website(message):

    bot.send_message(message.chat.id, 'Переход на сайт ts.kg:')
    bot.send_message(message.chat.id, 'https://ts.kg')


bot.polling()