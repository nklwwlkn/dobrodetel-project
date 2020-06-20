import vk
import json
import math
import time

from geopy.geocoders import Nominatim

now = str(time.time()).split('.')[0]

access_token = "28f1ebfa28f1ebfa28f1ebfad528835af6228f128f1ebfa761ce2e835425078a1233e1e"
session = vk.Session(access_token=access_token)
vkapi = vk.API(session)
geolocator = Nominatim(user_agent="dobrodetel")

radius = 30
street = ""

catalogList = []
savedPostsList = []


def convert_string_to_list(catalog):
    catalog_list = catalog.replace(',', ' ').split()
    return catalog_list


def get_product_list(category):
    print(len(category))
    all_category_post = []
    for product in category:
        posts_list = get_posts(owner_id='-109125816', vkapi=vkapi, count=10, query=product,
                               adress="Москва,Бобруйская улица 20")
        for post in posts_list:
            if not has_banned_words(post['post']):
                post_text = post['post']
                post_url = post['url']
                all_category_post.append({'post': post_text, 'url': post_url})
    return all_category_post


relevant_groups = [-109125816, -70298501, -112367858]


# Научиться получать все посты из группы CLOSE
# каждый пост форматировать в JSON {Location, posrt, url} CLOSE
# Написать функцию по парсингу постов из релевантных групп CLOSE
# Написать функцию бан-вордов
# Рассчитывать расстояние между двумя объектами CLOSE
# Добавить пагинацию
# Добавить то, что забыл


def has_banned_words(text):
    banned = ['Конкурс', 'конкурс', 'викторина', 'Викторина',
              'победил', 'Победил', 'победитель', 'Победитель', 'Розыгрыши', 'розыгрышы',
              'СТОП', 'Забрали', 'Отдано', 'Стоп', 'ЗАБРАЛИ', 'ОТДАНО', 'спасли', 'Спасли', 'СПАСЛИ', 'стоп', 'СПБ',
              'спб', 'СПб', 'Петербург', 'Санкт-Петербург']

    for word in banned:
        if word in text:
            return True
    return False


def difference(list1, list2):
    list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return list_dif


def get_posts(owner_id, vkapi, count, query, adress):
    global savedPostsList
    post_texts = []
    adress_user = convert_adress_to_coordinates(adress)

    convert_string_to_list("рис, еда, вода, пиво сухарики")

    posts_list = vkapi.wall.search(
        owner_id=owner_id, count=count, query=query, v=5.92)['items']

    for item in posts_list:
        if item['post_type'] == 'post':
            if not has_banned_words(item['text']):
                # проверить:
                print(int(item['date']), (int(now) - 72 * 60 * 60))
                if item['date'] > (int(now) - 150 * 60 * 60):
                    # проверить:
                    post = item['text']


                adress_distribution = parse_adress_from_photo(item)
                if adress_distribution and adress_user:
                    distance = haversine(adress_distribution, adress_user)
                    if distance <= radius * 1000:
                        post_texts.insert(0, {'post': item['text'], 'date': item['date'],
                                              'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])})
                        print(post)
                        print(distance)
                    """else:
                        post_texts.append({'post': item['text'], 'date': item['date'],
                                           'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])})

                else:
                    post_texts.append({'post': item['text'], 'date': item['date'],
                                       'url': 'https://vk.com/wall{}_{}'.format(item['owner_id'], item['id'])})"""

    for diff in difference(savedPostsList, post_texts):
        savedPostsList.append(diff)

    return post_texts


def convert_adress_to_coordinates(adress):
    location = geolocator.geocode(adress)
    if location:
        return location.latitude, location.longitude
    else:
        return None


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

                        return lat, long

        return None
    except:
        print("Проблема с парсингом адреса")
        return None


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


print(get_posts(owner_id='-109125816', vkapi=vkapi,
                count=50, query='молоко', adress=""))

"""def test():
    get_posts(owner_id='-109125816', vkapi=vkapi,
              count=20, query='Молоко', adress="")
    time.sleep(10)
    test()


test()"""
