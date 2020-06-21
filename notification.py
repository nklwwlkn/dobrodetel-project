import schedule
import requests
import datetime
from parse import *
from db import *

nows = datetime.datetime.now()

dbs = DBHelper()


def telegram_bot_sendtext(bot_message):
    bot_token = '948522010:AAG3dBL2W-NWPpdnOnuj-a15lOZ0dWlAv1o'
    list_id = dbs.get_all_user()
    for user_id in list_id:
        bot_chatID = str(user_id)
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        requests.get(send_text)


def report():
    dbs.setup()
    # dbs.get_all_user()
    print("Good joob")

    posts_list = get_posts(owner_id='-109125816', vkapi=vkapi,
                           count=10, query='хлеб', adress="Москва, м. Комсомольская")

    if len(posts_list) > 0:
        for post in posts_list:
            post_text = post['post']
            post_url = post['url']
            my_message = "Объявление: {} \nПерейти: {}".format(post_text, post_url)
            telegram_bot_sendtext(my_message)


schedule.every(10).seconds.do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
