from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from config import BOT_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
