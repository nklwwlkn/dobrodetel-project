import telebot
import logging
from parse import *
from telebot import types

bot = telebot.TeleBot('948522010:AAG3dBL2W-NWPpdnOnuj-a15lOZ0dWlAv1o')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет , это бот 'Добродетель' , расскажи , чего ты хочешь от этой жизни")
    bot.send_message(message.from_user.id, "Вы готовы отправиться в увлекательное приключение ?")
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Далее', callback_data='continue')  # кнопка
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Не интересно', callback_data='no-interesting')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, 'Ваш ответ: ',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "continue":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # Посмотреть задержку, вроде как не получается после edit'a сразу отправлять сообщение
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='Ваш ответ: Далее', reply_markup='')

    elif call.data == "no-interesting":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ваш ответ: Не '
                                                                                                     'интересно',
                              reply_markup='')


@bot.message_handler(commands=['help'])
def send_faq(message):
    bot.send_message(message.from_user.id, "Скоро мы запилим FAQ , но это не точно ((( !!!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Далее":
        bot.send_message(message.from_user.id, "Приятно, что вы готовы к общению. \n"
                                               "Ну что же, поведайте мне, где вы живете (ветка Метро)")
    elif message.text == "Помогите":
        bot.send_message(message.from_user.id, "Поможем !")
    elif message.text == "Парсинг":
        posts_list = get_posts(owner_id='-109125816', vkapi=vkapi, count=6, query='салат', adress="Набережная Волжской Флотилии 1")
        for post in posts_list:
            post_text = post['post']
            post_url = post['url']
            bot.send_message(message.from_user.id, "Объявление: {} \nПерейти: {}".format(post_text, post_url))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
