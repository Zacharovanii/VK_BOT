from dotenv import load_dotenv
from datetime import datetime
from os import getenv
from random import choice
from string import ascii_letters
from urllib.parse import urlparse, parse_qsl

import asyncio
from aiohttp import ClientSession
from aiofiles import open


load_dotenv()
VK_API = getenv('VK_API')
URL = "https://api.vk.com/method/wall.getById"


def random_letters(length):
    letters = ascii_letters
    return ''.join(choice(letters) for _ in range(length))


def isValidURL(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def getImg(img_url, session):
    async with open(random_letters(10)+'.jpeg', mode='wb') as f:
        filename = f.name
        photo = await session.get(img_url)
        async for chunk in photo.content.iter_chunked(1024):
            await f.write(chunk)
        return filename


async def getData(wall_url, session):
    try:
        posts = parse_qsl(urlparse(wall_url).query)[0][1].lstrip('wall')
    except IndexError:
        posts = wall_url.split('/')[-1].lstrip('wall')
    params = {'access_token': VK_API, 'posts': posts, "v": "5.199"}
    response = await session.get(URL, params=params)
    response = await response.json()
    response = response['response']['items']
    photos_url = [i['photo']['orig_photo']['url'] for i in response[0]['attachments'] if i['type'] == 'photo']
    text = response[-1]['text']
    date = datetime.fromtimestamp(response[-1]['date'])
    return text, date, photos_url


async def mainVK(wall_url):
    async with ClientSession() as session:
        text, date, photos_url = await getData(wall_url, session)
        tasks = [asyncio.create_task(getImg(url, session)) for url in photos_url]
        photos = await asyncio.gather(*tasks)
        return text, date, photos