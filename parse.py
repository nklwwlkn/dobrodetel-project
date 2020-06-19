import vk
import json
import math
from geopy.geocoders import Nominatim

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)
geolocator = Nominatim(user_agent="dobrodetel")
city = "Москва,"

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


def get_posts(owner_id, vkapi, count, query, adress):
    post_texts = []
    adress_coordinates = convert_adress_to_coordinates(city + adress)

    posts_list = vkapi.wall.search(
        owner_id=owner_id, count=count, query=query, v=5.92)['items']

    for item in posts_list:
        if item['post_type'] == 'post':
            post = item['text']

            post_texts.append([{'post': item['text'], 'date': item['date'],
                                'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])}])
        post = item['text']
        print(post + "\n")
        post_texts.append([post])
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
                        break

    except:
        print("Something went wrong...")


def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


print(get_posts(owner_id='-109125816', vkapi=vkapi, count=10, query='салат', adress="Набережная Волжской Флотилии 1"))
