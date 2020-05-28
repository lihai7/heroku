from telebot import types
import telebot
from lxml import html
import requests
import re

def parse_btc_to_usd():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url = 'https://bit.ly/36w63nL'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    take_btc = page.xpath('string(//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1])')
    return take_btc
parse_btc_to_usd()

def parse_weather():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    url = 'https://sinoptik.ua/погода-днепр-303007131'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    weather_now = page.xpath('string(//*[@id="bd1c"]/div[1]/div[1]/div[1]/p[2])')
    return(weather_now)

def parse_chance_of_rain():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    url = 'https://sinoptik.ua/погода-днепр-303007131'
    r = requests.get(url, headers=headers)
    page = html.fromstring(r.text)
    chance_of_rain = page.xpath('string(//*[@id="bd1c"]/div[1]/div[2]/table/tbody/tr[8])')
    chance_of_rain = chance_of_rain.replace('-','')  # Убираем "-"
    chance_of_rain = re.sub(r'\s','',chance_of_rain) # Убираем лишние пробелы
    return(chance_of_rain)
parse_chance_of_rain()
print(re.__version__)
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
        bot.send_message(message.chat.id, (f'Сейчас на улице {parse_weather()}\nВероятность осадков {parse_chance_of_rain()}%'))
    if message.text == 'Узнать курс биткоина':
        bot.send_message(message.chat.id, (f'1 BTC={parse_btc_to_usd()}USD'))
#Bot srart
bot.polling(none_stop=True)
