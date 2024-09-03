from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from database.db import initialize_db, close_db
from handlers import register_handlers
from config import BOT_TOKEN
from userbot import app

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


def start_bot():
    initialize_db()
    register_handlers(dp)
    try:
        app.start()
        executor.start_polling(dp, skip_updates=True)
    finally:
        close_db()
        app.stop()
