import schedule
import requests
import datetime
from parse import *
from db import *

nows = datetime.datetime.now()

dbs = DBHelper()


def telegram_bot_sendtext(bot_message):
    bot_token = '948522010:AAG3dBL2W-NWPpdnOnuj-a15lOZ0dWlAv1o'
    list_id, list_category = dbs.get_all_user()
    for user_id in list_id:
        print("Were GOOD !")
        bot_chatID = str(user_id)
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + str(bot_message)
        print(send_text)
        requests.get(send_text)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(551358615) + '&text=' + str(bot_message)
    response = requests.get(send_text)
    return response.json()


def report():
    dbs.setup()
    create_handler()
    post_handler()



def create_handler():
    posts_list = vkapi.wall.get(
            owner_id='-109125816', count=10, v=5.92)['items']

    list_id, list_category = dbs.get_all_user()
    data_dict = {}
    if len(posts_list) > 0:
        for item in posts_list:
            post_url = 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])
            post_date = item['date']
            data_dict[post_date] = post_url

    list_keys = list(data_dict.keys())
    list_keys.sort()
    for user_id in list_id:
        dbs.create_posts(user_id, list_keys[len(list_keys)-1], data_dict[list_keys[len(list_keys)-1]])


def post_handler():
    posts_list = vkapi.wall.get(
        owner_id='-109125816', count=10, v=5.92)['items']

    list_id, list_category = dbs.get_all_user()
    data_dict = {}
    if len(posts_list) > 0:
        for item in posts_list:
            post_url = 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])
            post_date = item['date']
            data_dict[post_date] = post_url

    list_keys = list(data_dict.keys())
    list_keys.sort()
    time_list, url_list = dbs.get_all_posts()
    if int(time_list[0]) < list_keys[len(list_keys) - 1]:
        print("YOU HERE !")
        for user_id in list_id:
            dbs.update_post(user_id, str(list_keys[len(list_keys) - 1]), data_dict[list_keys[len(list_keys) - 1]])
        url_user = data_dict[list_keys[len(list_keys) - 1]].split("-")[1]
        post = vkapi.wall.getById(posts='-{}'.format(url_user), v=5.92)
        for item in post:
            print("YOU can do it !! !")
            message = "Новое Объявление: " + item['text'] + "\nПерейти: " + data_dict[list_keys[len(list_keys) - 1]]
            telegram_bot_sendtext(message)
            break


schedule.every(60).seconds.do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
