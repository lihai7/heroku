from telebot import types
import telebot
from lxml import html
import requests
import re

def parse_btc_to_usd():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url = 'https://www.google.com/search?sxsrf=ALeKk03xACIxe2MEXHC1GZAhCfv9hAFW8Q%3A1590711331143&ei=I1TQXuymCMKimwWC_LToCQ&q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B4%D0%BD%D0%B5%D0%BF%D1%80+%D1%86%D0%B5%D0%BB%D1%8C%D1%81%D0%B8%D0%B9&oq=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%B4%D0%BD%D0%B5%D0%BF%D1%80+%D1%86%D0%B5%D0%BB%D1%8C%D1%81%D0%B8%D0%B9&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCAAjoECAAQRzoMCCMQJxCdAhBGEIACOgQIIxAnOgUIABCDAToCCAA6BggAEBYQHlCaiQFY75wBYLKeAWgAcAF4AIABmQKIAZAIkgEFMS42LjGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwisxNS-5dfpAhVC0aYKHQI-DZ0Q4dUDCAw&uact=5'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    take_btc = page.xpath('string(//*[@id="wob_tm"])')

    return take_btc
parse_btc_to_usd()

def parse_weather():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    url = 'https://bit.ly/2Maoc13'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    weather_now = page.xpath('string()')
   
    return(weather_now)
parse_weather()

def parse_chance_of_rain():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    url = 'https://google.com/search?q=погода+днепр&oq=погода+днепр'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    chance_of_rain = page.xpath('string(//*[@id="wob_pp"])')
    chance_of_rain = chance_of_rain.replace('-','')  # Убираем "-"
    chance_of_rain = re.sub(r'\s','',chance_of_rain) # Убираем лишние пробелы

    return(chance_of_rain)
parse_chance_of_rain()
###
#
bot = telebot.TeleBot('1159436936:AAG1FkCcfb6npHdRyYluwzLMdMGRfraIzhg')
#
@bot.message_handler(commands=['start'])
def welcome(message):
    # bot.send_message(message.chat.id, 'Привет, я буду отправлять тебе погоду/курс биткоина.')
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать погоду")
    item2 = types.KeyboardButton("Узнать курс биткоина")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привет, я буду отправлять тебе погоду/курс биткоина".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def weather(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, (f'Сейчас на улице {parse_weather()}.\nВероятность осадков {parse_chance_of_rain()}%'))
    if message.text == 'Узнать курс биткоина':
        bot.send_message(message.chat.id, (f'1 BTC={parse_btc_to_usd()}USD'))
#Bot srart
bot.polling(none_stop=True)
