import telebot
from random import *
import json
import requests
from telebot import types

films=[]
API_URL='https://7012.deeppavlov.ai/model'

# Записываем токен бота из файла который не будет доступен внешним пользователям
with open("bot.secr", "r", encoding="UTF-8") as fn:
    token = fn.read()

with open("start_text.txt", "r", encoding="UTF-8") as fn:
    st_txt = fn.read()

API_TOKEN = token
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Вы запустили правовую экспертную систему", reply_markup=markup)


@bot.message_handler(commands=['вопрос'])
def wiki(message):
    quest = message.text.split()[1:]
    qq = " ".join(quest)
    data = {'question_raw': [qq]}
    try:
        res = requests.post(API_URL,json=data,verify=False).json()
        bot.send_message(message.chat.id, res)
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")

@bot.message_handler(commands=['консультация'])
def request_specialist(message):
    bot.send_message(message.chat.id,"Ваш запрос получен. Верьте что мы сделаем все возможное и невозможное чтобы вам помочь.")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Задать вопрос':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Предупреждение!!!')
        btn2 = types.KeyboardButton('Информация')
        btn3 = types.KeyboardButton('Запрос к специалисту')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота


    elif message.text == 'Предупреждение!!!':
        try:
            bot.send_message(message.chat.id,st_txt)

        except:
            bot.send_message(message.chat.id,"Что то пошло не так")

    elif message.text == 'Информация':
        bot.send_message(message.from_user.id, 'Если вы хотите задать вопрос встроенной в помощника нейросети то используйте форму /вопрос (Далее ваш текст без скобок)')

    elif message.text == 'Запрос к специалисту':
        bot.send_message(message.from_user.id, 'Если вам нужна консультация эксперта человеке, то воспользуйтесь формой /консультация (Далее ваш текст без скобок). Как только ваш запрос будет изучен и разработан, вам придет уведомление с ответом' )

bot.polling()