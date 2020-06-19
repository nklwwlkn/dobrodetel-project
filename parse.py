import vk
import json

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)


relevant_groups = [-109125816, -70298501, -112367858]

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


def get_posts(owner_id, vkapi, count, query):
    post_texts = []

    posts_list = vkapi.wall.search(
        owner_id=owner_id, count=count, query=query, v=5.92)['items']

    for item in posts_list:
        post = item['text']

        post_texts.append([{'post': item['text'], 'date': item['date'],
                            'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])}])

    return post_texts


print(get_posts(owner_id='-109125816', vkapi=vkapi, count=10, query='Салат'))
