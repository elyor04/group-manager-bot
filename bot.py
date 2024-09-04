from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from database.db import initialize_db, close_db
from handlers import register_handlers
from config import BOT_TOKEN
from userbot import app

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    initialize_db()
    register_handlers(dp)
    try:
        await app.start()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        close_db()
        await app.stop()
