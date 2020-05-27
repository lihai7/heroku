from telebot import types
import telebot
from functions import parse_btc_to_usd, parse_weather, parse_chance_of_rain
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
