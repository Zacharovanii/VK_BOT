from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl
from datetime import datetime
from random import choice
from string import ascii_letters
from os import getenv
import requests


def random_letters(length):
    letters = ascii_letters
    return ''.join(choice(letters) for _ in range(length))


load_dotenv()
VK_API = getenv('VK_API')


def isValidURL(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def getInfo(wall_url):
    try:
        posts = parse_qsl(urlparse(wall_url).query)[0][1].lstrip('wall')
    except IndexError:
        posts = wall_url.split('/')[-1].lstrip('wall')
    url = "https://api.vk.com/method/wall.getById"
    response = requests.get(url, params={'access_token': VK_API, 'posts': posts, "v": "5.199"}, timeout=10).json()['response']['items']
    text = response[-1]['text']
    date = datetime.fromtimestamp(response[-1]['date'])
    photos = []
    for photo in response[0]['attachments']:
        if photo['type'] == 'photo':
            # photo_url = requests.get(photo['photo']['orig_photo']['url'])
            name = random_letters(10) + '.jpeg'
            # image = Image.open(BytesIO(photo_url.content))
            # image.save(name, 'jpeg')
            photos.append(name)

            photo_url = requests.get(photo['photo']['orig_photo']['url'], stream=True)

            if photo_url.status_code == 200:
                with open(name, 'wb') as file:
                    # Запись файла по частям
                    for chunk in photo_url.iter_content(512):
                        file.write(chunk)
            else:
                # Обработка ошибок при невозможности загрузки изображения
                print(f'Загрузить изображение не удалось: код ответа сервера {photo_url.status_code}')

    return text, date, photos