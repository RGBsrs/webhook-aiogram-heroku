import logging
import httpx

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
    photo = await bot.get_file(photo_id)
    ext = photo.file_path.split('.')[-1]
    await photo.download(f'{photo_id}.{ext}')
    async with httpx.AsyncClient() as client:
        async with open(f'{photo_id}.{ext}','rb') as file:
            files = {f'{photo_id}.{ext}': file}
            url = 'https://api.ocr.space/parse/image'
            headers = {'apikey': API_KEY}
            resp = client.post(url, headers=headers, files=files)
    if resp:
        await message.answer(resp.json())
    else:
        await message.answer('Some troubles')


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
