import schedule
import requests
import datetime
from parse import *

now = datetime.datetime.now()

def telegram_bot_sendtext(bot_message):
    bot_token = '948522010:AAG3dBL2W-NWPpdnOnuj-a15lOZ0dWlAv1o'
    bot_chatID = '551358615'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def report():
    posts_list = get_posts(owner_id='-109125816', vkapi=vkapi,
              count=10, query='хлеб', adress="Москва, м. Комсомольская")

    if len(posts_list) > 0:
        for post in posts_list:
            post_text = post['post']
            post_url = post['url']
            my_message = "Объявление: {} \nПерейти: {}".format(post_text, post_url)
            telegram_bot_sendtext(my_message)


schedule.every().day.at("0{}:{}:{}".format(now.hour,now.minute,now.second + 20)).do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
