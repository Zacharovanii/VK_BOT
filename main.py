import logging
import sys
from VK import *
from os import remove


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile


TG_API = getenv('TG_API')


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer("Я бот для анализа постов вк. На данный момент я умею считывать текст, дату и картинки поста")


@dp.message()
async def echo_handler(message: Message) -> None:
    posts = isValidURL(message.text)
    if posts:
        text, date, photos = await mainVK(posts)
        first = html.bold("Текст поста:")
        second = html.bold(f"Время создания: {date}")
        await message.answer(f"{first}\n{text}\n\n{second}")
        if photos:
            for photo in photos:
                await message.answer_document(FSInputFile(photo))
                remove(photo)
    else:
        await message.answer(f"Невалидная ссылка, попробуй еще раз")


async def main() -> None:
    bot = Bot(token=TG_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())