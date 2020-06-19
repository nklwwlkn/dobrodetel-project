import vk
import json

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)

# Научиться получать все посты из группы
# каждый пост форматировать в JSON {Location, posrt, url}
# Написать функцию по парсингу постов из релевантных групп
# Написать функцию бан-вордов
# Добавить то, что забыл

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
        print(post + "\n")
        post_texts.append([post])
        try:
            attachments = item['attachments']
            if attachments:
                for attach in attachments:
                    type = attach['type']
                    if type == "photo":
                        photo = attach['photo']
                        if photo['lat']:
                            lat = photo['lat']
                            long = photo['long']
                            print("Гео: {}".format(lat))
                            break

        except:
            print("Error")

    return post_texts


def search_posts(owner_id, vkapi, count, search_text):
    posts = []

    posts_list = vkapi.wall.search(owner_id=owner_id, count=50)


print(get_posts(owner_id='-109125816', vkapi=vkapi, count=50))
