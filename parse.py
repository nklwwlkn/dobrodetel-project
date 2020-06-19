import vk
import json

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)


"""  def is_baned_words(text):
    banned_words = ['Продам', 'продам', 'конкурс', 'Конкурс']
        for banned in banned_words:
            if banned in text:
                return True
    return False
 """


def get_posts(owner_id, vkapi, count):
    post_texts = []

    posts_list = vkapi.wall.get(
        owner_id=owner_id, count=count, v=5.92)['items']

    for item in posts_list:
        post = item['text']

        post_texts.append([post])

    return post_texts


print(get_posts(owner_id='-109125816', vkapi=vkapi, count=10))
