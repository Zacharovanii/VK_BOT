from dotenv import load_dotenv
from os import getenv
from urllib.parse import urlparse, parse_qsl
from datetime import datetime
from PIL import Image
from io import BytesIO
from random import choice
from string import ascii_letters
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
    posts = parse_qsl(urlparse(wall_url).query)[0][1].lstrip('wall')
    url = "https://api.vk.com/method/wall.getById"
    response = requests.get(url, params={'access_token': VK_API, 'posts': posts, "v": "5.199"}).json()['response']['items']

    text = response[-1]['text']
    date = datetime.fromtimestamp(response[-1]['date'])
    photos = []
    for photo in response[0]['attachments']:
        if photo['type'] == 'photo':
            photo_url = requests.get(photo['photo']['orig_photo']['url'])
            name = random_letters(10) + '.jpeg'
            image = Image.open(BytesIO(photo_url.content))
            image.save(name, 'jpeg')
            photos.append(name)

    return text, date, photos
