import telebot
import logging
from parse import *
from telebot import types
from time import sleep

bot = telebot.TeleBot('948522010:AAG3dBL2W-NWPpdnOnuj-a15lOZ0dWlAv1o')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

# GLOBAL Param
user_street = 'Москва, Бобруйская улица 20'
user_radius = 5
user_category = ["Молоко", "Квас", "Колбаса"]

"""
@bot.callback_query_handler(func=lambda call: call.data == 'continue')
def callback_inline_first(message):
    ...
"""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     "Я создана для помощи людям, которые нуждаются в еде. С моей помощью вы сможете найти предложения об безвозмездной раздачи еды, которые интересны именно вам!")
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Далее', callback_data='continue')  # кнопка
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id,
                     'Для начала, давайте заполним первичную информацию о вас! \nДля продолжения нажмите "Далее"',
                     reply_markup=keyboard)


def get_from_user_posts(user_id, address):
    global user_category
    posts_list = get_product_list(user_category)
    # posts_list = get_posts(owner_id='-109125816', vkapi=vkapi, count=10, query='салат', adress=address)
    if len(posts_list) > 0:
        for post in posts_list:
            post_text = post['post']
            post_url = post['url']
            bot.send_message(user_id, "Объявление: {} \nПерейти: {}".format(post_text, post_url))
            sleep(1)
            # lat, lon = convert_adress_to_coordinates("Набережная Волжской Флотилии 1")
            # bot.send_location(message.chat.id, latitude=lat, longitude=lon)
    else:
        bot.send_message(user_id, "К сожалению,не нашлось подходящих продуктов.")


@bot.callback_query_handler(func=lambda call: True)
def callback_continue(call):
    global user_street
    if call.data == "continue":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Отлично, начнём наше знакомство', reply_markup='')
        sleep(1)
        bot.send_message(call.from_user.id, "Где Вы проживаете? (Москва, м. Комсомольская)")
        bot.register_next_step_handler(call.message, get_user_street)
    elif call.data == "post-yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Благодарим за ответ.', reply_markup='')
        sleep(1)
        bot.send_message(call.from_user.id, 'Вот, что я смогла найти для Вас:')
        get_from_user_posts(call.from_user.id, user_street)
    elif call.data == "post-no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Благодарим за ответ.', reply_markup='')
        sleep(1)
        bot.send_message(call.from_user.id, 'Будем ждать вас!')


def get_user_street(message):
    global user_street
    user_street = message.text
    bot.send_message(message.from_user.id, 'В радиусе скольких километров Вам хотелось бы узнавать об актуальных предложениях (3)?')
    bot.register_next_step_handler(message, get_user_radius)


def get_user_radius(message):
    global user_radius
    user_radius = float(message.text)
    bot.send_message(message.from_user.id, 'Какие продукты Вам интересны? (молоко, рис, пицца)')
    bot.register_next_step_handler(message, get_user_category)


def get_user_category(message):
    global user_category
    user_category = convert_string_to_list(message.text)
    print("User category lens: ", len(user_category))
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='post-yes')  # кнопка
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='post-no')  # кнопка
    keyboard.add(key_no)  # добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id, "Вы хотите получить список постов ?", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_faq(message):
    bot.send_message(message.from_user.id,
                     "Команда: /start - знакомит с ботом и предлагает повзаимодейтсвовать с ним \n"
                     "Слово: Посты - выводит все посты, созданно для теста \n"
                     )


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Посты":
        global user_street
        get_from_user_posts(message.from_user.id, user_street)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
