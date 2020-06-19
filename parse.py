import vk
import json
from geopy.geocoders import Nominatim

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)
geolocator = Nominatim(user_agent="dobrodetel")

relevant_groups = [-109125816, -70298501, -112367858]

# Научиться получать все посты из группы
# каждый пост форматировать в JSON {Location, posrt, url}
# Написать функцию по парсингу постов из релевантных групп
# Написать функцию бан-вордов
# Добавить то, что забыл


""" def has_banned_words(text):
    banned = ['Конкурс', 'конкурс', 'викторина', 'Викторина',
              'победил', 'Победил', 'победитель', 'Победитель', 'Розыгрыши', 'розыгрышы']

    for word in banned:
        if word in text:
            return True
    return False """


def get_posts(owner_id, vkapi, count, query, adress):
    post_texts = []
    lat, long = convert_adress_to_coordinates(adress)

    posts_list = vkapi.wall.search(
        owner_id=owner_id, count=count, query=query, v=5.92)['items']

    for item in posts_list:
        if item['post_type'] == 'post':
            post = item['text']

            post_texts.append([{'post': item['text'], 'date': item['date'],
                                'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])}])
        post = item['text']
        print(post + "\n")
        parse_adress_from_photo(item)

    return post_texts


def convert_adress_to_coordinates(adress):
    location = geolocator.geocode(adress)
    print(location.latitude, location.longitude)
    return location.latitude, location.longitude


def parse_adress_from_photo(item):
    try:
        attachments = item['attachments']
        if attachments:
            for attach in attachments:
                type_attachment = attach['type']
                if type_attachment == "photo":
                    photo = attach['photo']
                    if photo['lat']:
                        lat = photo['lat']
                        long = photo['long']
                        print("Гео: {}".format(lat))
                        break

    except:
        print("Error")


print(get_posts(owner_id='-109125816', vkapi=vkapi, count=10,
                query='Конкурс', adress="Набережная Волжской Флотилии 1"))
