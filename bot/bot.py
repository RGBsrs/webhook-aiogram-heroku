import logging
import requests

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.answer(message.text)

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    photo_id = message.photo[0].file_id
    photo_info = await bot.get_file(photo_id)
    await bot.download_file(photo_info.file_path, 'photo/test.jpg')
    
    files = {'file':  open('photo/test.jpg', 'rb')}
    url = 'https://api.ocr.space/parse/image'
    headers = {'apikey': API_KEY}
    resp = requests.post(url, headers=headers, files=files)

    await message.answer(resp.status_code)


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
