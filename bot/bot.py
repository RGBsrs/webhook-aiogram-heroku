import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import *
from services.parser import PdaParser, HabrParser

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
pda_parser = PdaParser()
habr_parser = HabrParser()


@dp.message_handler(commands=['4pda'])
async def echo(message: types.Message):
    resp = await pda_parser.get_response()
    if resp.status_code == 200:
        posts = await pda_parser.process_html()
        logging.warning('make asnwer')
        await message.answer(posts)

@dp.message_handler(commands=['habr'])
async def echo(message: types.Message):
    resp = await habr_parser.get_response()
    if resp.status_code == 200:
        posts = await pda_parser.process_html()
        logging.warning('make asnwer')
        await message.answer(posts)

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):

    await message.photo[-1].download('test.jpg')

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
